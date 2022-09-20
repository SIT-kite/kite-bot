import json
from aiohttp.web import *
import bot
from txc_entity import TxcHookEntity, POST_CREATED

app = Application()


def build_txc_post_message(message: TxcHookEntity):
    return f"""
创建时间: {message.created_at}
消息类型: {message.type}
消息内容: {message.payload['post'].content}
""".strip()


async def handle(request: Request):
    bs = await request.content.read()
    content = bs.decode('utf-8')
    txc_message: TxcHookEntity = TxcHookEntity.from_dict(json.loads(content))
    if txc_message.type == POST_CREATED:
        await bot.send_text_message(build_txc_post_message(txc_message))
    return Response(status=200)


app.add_routes([
    post('/feedback_hook', handle)
])


def run_web_server(loop):
    run_app(app, loop=loop)


__all__ = [
    'run_web_server'
]
