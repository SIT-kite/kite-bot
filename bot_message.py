import datetime

from txc_entity import TxcHookEntity


def build_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def build_txc_post_message(message: TxcHookEntity):
    return f"""
创建时间: {message.created_at}
消息类型: {message.type}
消息内容: {message.payload['post'].content}
""".strip()
