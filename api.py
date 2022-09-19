from aiohttp.web import *
import bot

app = Application()

async def handle(request: Request):
    print('收到反馈')
    await bot.send_text_message(request.content)
    return Response(status=200)

app.add_routes([
    post('/feedback_hook', handle)
])

def run_web_server(loop):
    run_app(app, loop=loop)

__all__ = [
    'run_web_server'
]