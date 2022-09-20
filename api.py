import json
from aiohttp.web import *
import bot
import bot_message
from txc_entity import TxcHookEntity, POST_CREATED

app = Application()


async def txc_hook_handler(request: Request, extra_msg: str):
    bs = await request.content.read()
    content = bs.decode('utf-8')
    txc_message: TxcHookEntity = TxcHookEntity.from_dict(json.loads(content))
    if txc_message.type == POST_CREATED:
        await bot.send_text_message(bot_message.build_txc_post_message(txc_message, extra_msg))
    return Response(status=200)


app.add_routes([
    post('/webhook/txc/feedback', lambda r: txc_hook_handler(r, "消息来源：反馈")),
    post('/webhook/txc/qa', lambda r: txc_hook_handler(r, "消息来源：问答"))
])


def run_web_server(loop):
    run_app(app, loop=loop)


__all__ = [
    'run_web_server'
]
