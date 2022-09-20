import datetime

from txc_entity import TxcHookEntity


def build_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def build_txc_post_message(message: TxcHookEntity, extra_msg: str = ''):
    post = message.payload['post']
    return f"""
兔小巢消息
创建时间: {message.created_at}
消息类型: {message.type}
消息链接: {post.post_url}
消息内容: {post.content}
{extra_msg}
""".strip()
