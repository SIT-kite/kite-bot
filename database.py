import asyncio
from dataclasses import dataclass

import asyncpg
from asyncpg import Connection, Record
from typing import *
import datetime
from dataclasses_json import dataclass_json

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


async def main():
    await connect()
    print(await select_top_3_notice())
    await close()


if __name__ == '__main__':
    asyncio.run(main())
