import json
from aiohttp.web import *
import bot
import txc_entity

app = Application()

async def handle(request: Request):
    bs = await request.content.read()
    content = bs.decode('utf-8')
    e = txc_entity.HookEntity.fromDict(json.loads(content))
    payload: txc_entity.PostEntity = e.payload
    await bot.send_text_message(payload.content)
    return Response(status=200)

app.add_routes([
    post('/feedback_hook', handle)
])

def run_web_server(loop):
    run_app(app, loop=loop)

__all__ = [
    'run_web_server'
]