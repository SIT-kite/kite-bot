from dataclasses import dataclass
from typing import *
from datetime import datetime, timezone, timedelta
import calendar
from file_read_backwards import FileReadBackwards
import util

from config import current_config

nginx_log_file = current_config.nginx_log_file


@dataclass
class RequestHeader:
    method: str
    url: str
    version: str


@dataclass
class NginxLogItem:
    ip_addr: str
    time: datetime
    header: RequestHeader
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
                minutes=int(tz[3:]),
            )
        )
    )
    header_method, header_url, header_version = header.split(' ')
    return NginxLogItem(
        ip_addr=ip_addr,
        time=dt_with_tz,
        header=RequestHeader(
            method=header_method,
            url=header_url.split('?')[0],
            version=header_version,
        ),
        status=int(status),
        unknown_num=unknown_num,
        user_agent=ua,
    )


# 建立月份字符串索引
month_table = {}
for i, v in enumerate(calendar.month_abbr):
    month_table[v] = i


def generate_recently_log(before_delta: timedelta = timedelta(days=30)):
    end = util.now_utc_time()
    start = end - before_delta
    with FileReadBackwards(nginx_log_file, encoding="utf-8") as frb:
        for line in frb:
            log_line = parse_line(line)
            if start <= log_line.time:
                yield log_line
            else:
                break


def count_generator(gen: Generator):
    cnt = 0
    for _ in gen:
        cnt += 1
    return cnt


def count_request_num(before_delta: timedelta):
    return count_generator(generate_recently_log(before_delta))


def draw_recently_24hour():
    import matplotlib.pyplot as plt
    from io import BytesIO
    dic = {}
    for log in generate_recently_log(timedelta(days=1)):
        t = log.time
        if t.hour not in dic.keys():
            dic[t.hour] = 0
        dic[t.hour] += 1
    plt.clf()
    plt.plot(
        list(map(lambda x: f'{x}', reversed(dic.keys()))),
        list(reversed(dic.values())),
    )

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf


def api_count_order(gen: Generator):
    result = {}
    for log in gen:
        url = log.header.url
        if not url.startswith('/api/v2'):
            continue
        nu = '/'.join(url.split('/')[:4])
        if nu not in result.keys():
            result[nu] = 0
        result[nu] += 1
    return result

def get_diff_ua(len: int)->List[str]:
    gen = generate_recently_log()
    s = set()
    for log in gen:
        s.add(log.user_agent)
        if(len(s)>=100):
            return list(s)
    return list(s)