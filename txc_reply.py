import asyncio
import time
from aiohttp import *
from typing import *


def gen_uuid():
    from random import random
    uuid = ''
    for ii in range(32):
        if ii == 8 or ii == 20:
            uuid += '-'
            uuid += hex(int(random() * 16) | 0)[2:]
        elif ii == 12:
            uuid += '-'
            uuid += '4'
        elif ii == 16:
            uuid += '-'
            uuid += hex(int(random() * 4) | 8)[2:]
        else:
            uuid += hex(int(random() * 16) | 0)[2:]
    return uuid


product_id = ''
openid = ''
nickname = ''

session = None  # type: Optional[ClientSession]


async def login():
    await session.post(
        proxy='http://127.0.0.1:10888',
        url=f'https://support.qq.com/products/{product_id}',
        data={
            'openid': openid,
            'nickname': nickname,
            'avatar': 'https://txc.qq.com/static/desktop/img/products/def-product-logo.png',
        }
    )
    # for i in session.cookie_jar:
    #     print(i)

    # print(session.cookie_jar.filter_cookies(request_url=URL('http://qq.com')))



async def init_user_info():
    return await session.get(
        proxy='http://127.0.0.1:10888',
        url=f'https://support.qq.com/login/init_user_info/{product_id}?_={int(time.time() * 1000)}',
        cookies={
            '_horizon_sid': gen_uuid(),
            '_horizon_uid': gen_uuid(),
            '_tc_unionid': gen_uuid(),
        }
    )

from yarl import URL
async def reply_post(post_id: str, msg: str):
    url = f'https://support.qq.com/api/v1/{product_id}/posts/{post_id}/replies'
    return await session.post(
        proxy='http://127.0.0.1:10888',
        url=url,
        json={
            'categories': [],
            'image_upload_type': "file",
            'images': [],
            'parent_reply_id': None,
            'text': msg,
            'user_contacts': []
        },
        cookies={
            '_horizon_sid': gen_uuid(),
            '_horizon_uid': gen_uuid(),
            '_tc_unionid': gen_uuid(),
        }
    )


async def main():
    global session
    async with ClientSession(
            headers={
                "Cache-Control": "max-age=0",
                "Host": "support.qq.com",
                "Connection": "keep-alive",
                "sec-ch-ua": "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"",
                "sec-ch-ua-mobile": "?0",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/105.0.0.0 Safari/537.36",
                "sec-ch-ua-platform": "\"Windows\"",
                "Origin": "https://support.qq.com",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
            },
    ) as session1:
        session = session1
        await login()
        # await init_user_info()

        s = await reply_post('', '')
        print(await s.text())


asyncio.run(main())
