from dataclasses import dataclass
from typing import *
from datetime import datetime, timezone, timedelta
import calendar
from file_read_backwards import FileReadBackwards
import util

from config import current_config

nginx_log_file = current_config.nginx_log_file


@dataclass
class NginxLogItem:
    ip_addr: str
    time: datetime
    header: str
    status: int
    unknown_num: int
    user_agent: str


def split_parse(s: List[str], _line: str):
    """
    :param s: [' - ', ' ']
    :param _line: ”ab - c d“
    :return: ['ab', 'c', 'd']
    """
    result = []
    p = 0
    for si in s:
        ii = _line.find(si, p)
        result.append(_line[p:ii])
        p = ii + len(si)
    result.append(_line[p:])
    return result


def parse_line(_line: str):
    ip_addr, access_datetime, header, status, unknown_num, ua = split_parse(
        [' - - ', ' "', '" ', ' ', ' "-" "'],
        _line[:-1],
    )
    day, month, year, hour, minute, second, tz = split_parse(['/', '/', ':', ':', ':', ' '], access_datetime[1:-1])
    dt_with_tz = datetime(
        year=int(year),
        month=month_table[month],
        day=int(day),
        hour=int(hour),
        minute=int(minute),
        second=int(second),
        tzinfo=timezone(
            offset=timedelta(
                hours=int(tz[0:3]),
                minutes=int(tz[3:]))
        )
    )
    return NginxLogItem(
        ip_addr=ip_addr,
        time=dt_with_tz,
        header=header,
        status=int(status),
        unknown_num=unknown_num,
        user_agent=ua,
    )


# 建立月份字符串索引
month_table = {}
for i, v in enumerate(calendar.month_abbr):
    month_table[v] = i


def read_recently_log(before_delta: timedelta):
    cnt = 0
    end = util.now_utc_time()
    start = end - before_delta
    with FileReadBackwards(nginx_log_file, encoding="utf-8") as frb:
        for line in frb:
            log_line = parse_line(line)
            if start <= log_line.time:
                cnt += 1
            else:
                break
    return cnt