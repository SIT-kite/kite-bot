import json
from aiohttp.web import *
import bot
import bot_message
from txc_entity import TxcHookEntity, POST_CREATED
from config import current_config
from telebot.types import *
from urllib.parse import quote
app = Application()


async def txc_hook_handler(request: Request, extra_msg: str):
    bs = await request.content.read()
    content = bs.decode('utf-8')
    txc_message: TxcHookEntity = TxcHookEntity.from_dict(json.loads(content))
    if txc_message.type == POST_CREATED:
        msg = bot_message.build_txc_post_message(txc_message, extra_msg)
        post_url = txc_message.payload['post'].post_url
        await bot.bot.send_message(
            chat_id=current_config.bot.chat_id,
            text=msg,
            reply_markup=InlineKeyboardMarkup(
                keyboard=[[
                    InlineKeyboardButton(
                        text='立即回复',
                        url=f'https://kite.sunnysab.cn/txc/reply?post_url={quote(post_url)}',
                    )
                ]]
            ),
        )
    return Response(status=200)


async def txc_reply_page(request: Request):
    user = current_config.reply_user
    query = request.query
    response_text = f"""
<html>
    <head></head>
    <body>
        <form method="post" action="{query['post_url']}">
            <input type="hidden" name="openid" value="{user.openid}">
            <input type="hidden" name="nickname" value="{user.nickname}">
            <input type="hidden" name="avatar" value="{user.avatar}">
            <button hidden type="submit">
          </form>
          <script>
            document.getElementsByTagName('form')[0].submit();
          </script>
    </body>
</html>
    """
    return Response(
        status=200,
        body=response_text,
        content_type='text/html',
        charset='utf-8'
    )


app.add_routes([
    post('/webhook/txc/feedback', lambda r: txc_hook_handler(r, "消息来源：反馈")),
    post('/webhook/txc/qa', lambda r: txc_hook_handler(r, "消息来源：问答")),
    get('/txc/reply', txc_reply_page),
])


def run_web_server(loop):
    run_app(app, loop=loop)


__all__ = [
    'run_web_server'
]

if __name__ == '__main__':
    run_app(app)
