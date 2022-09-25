import asyncio
import json

import asyncpg
from asyncpg import Connection
from typing import *
import datetime
from dataclasses_json import dataclass_json, config
from dataclasses import dataclass, field

from config import current_config

db = current_config.database
conn = None  # type: Optional[Connection]


async def connect():
    global conn
    conn = await asyncpg.connect(
        user=db.username,
        password=db.password,
        database=db.database,
        host=db.host,
        port=db.port,
    )


async def close():
    await conn.close()


@dataclass_json
@dataclass
class NoticeRecord:
    publish_time: datetime.datetime
    title: str
    content: str


async def select_top_3_notice() -> List[NoticeRecord]:
    values = await conn.fetch("""
            SELECT publish_time, title, content
            FROM notice
            ORDER BY publish_time DESC
            LIMIT 3;
    """)
    return list(map(lambda x: NoticeRecord.from_dict(dict(x)), values))


@dataclass_json
@dataclass
class CollegeRate:
    college: str
    use_count: int
    total: int
    rate: str


async def select_college_rate() -> List[CollegeRate]:
    values = await conn.fetch("""
            select *, text(round(use_count * 1.0 / total * 100, 2)) || '%' as rate
            from 
                (select college, count(last_seen) as use_count, count(*) as total
                from freshman.students s
                group by college) t
            order by rate desc;
            """)
    return list(map(lambda x: CollegeRate.from_dict(dict(x)), values))


async def select_user_count() -> int:
    values = await conn.fetch("""
        SELECT count(*)
        FROM "user".account;
    """)
    return values[0]['count']


@dataclass_json
@dataclass
class BoardPictureRecord:
    id: str
    uid: str
    path: str
    thumbnail: str


async def select_board_picture_random() -> Optional[BoardPictureRecord]:
    values = await conn.fetch("""
        select *
        from board.picture
        where random() < 0.01
        limit 1;
        """)
    if len(values) > 0:
        return BoardPictureRecord.from_dict(values[0])
    else:
        return None


@dataclass_json
@dataclass
class RouteRecord:
    page: str
    param: str = ''


@dataclass_json
@dataclass
class UseStatisticRecord:
    route: RouteRecord = field(
        metadata=config(
            field_name='params',
            decoder=lambda x: RouteRecord(page='', param='') if x == '{}' else RouteRecord.from_json(x),
        ))
    count: int = field(metadata=config(field_name='hit'))


async def use_statistic(start: datetime.datetime, end: datetime.datetime) -> List[UseStatisticRecord]:
    values = await conn.fetch("""
        select params, count(*) as hit
        from public.history
        where ts >= $1
          and ts <= $2
        group by params
        order by hit desc;
    """, start, end)
    return list(map(lambda x: UseStatisticRecord.from_dict(x), values))


async def main():
    import util
    await connect()
    end_time = util.now_utc_time()
    start_time = end_time - datetime.timedelta(days=1)
    a = await use_statistic(start_time, end_time)
    print(a)
    await close()


if __name__ == '__main__':
    asyncio.run(main())
