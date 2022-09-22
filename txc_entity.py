from dataclasses import dataclass, field
from datetime import datetime
import json
from typing import *

from dataclasses_json import dataclass_json, config

POST_CREATED = 'post.created'
POST_UPDATED = 'post.updated'
REPLY_CREATED = 'reply.created'
REPLY_UPDATED = 'reply.updated'


@dataclass_json
@dataclass
class PostEntity:
    id: str
    product_id: str
    nick_name: str
    content: str
    created_at: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat
        )
    )
    updated_at: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat
        )
    )
    post_url: str


@dataclass_json
@dataclass
class ReplyEntity:
    content: str


def payload_parser(payload: Dict[str, any]):
    result = {}
    for k, v in payload.items():
        if k == 'post':
            result[k] = PostEntity.from_dict(v)
        elif k == 'reply':
            result[k] = ReplyEntity.from_dict(v)
    return result


@dataclass_json
@dataclass
class TxcHookEntity:
    id: str
    type: str
    created_at: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat
        )
    )

    payload: Dict[str, Union[PostEntity, ReplyEntity]] = field(
        metadata=config(
            decoder=lambda x: payload_parser(x),
        )
    )


if __name__ == '__main__':
    a = b'{"id":"36601f779a56dfde511045ade752b837","type":"post.created","payload":{"post":{' \
        b'"id":"166360302733603118","product_id":377648,"has_admin_reply":false,' \
        b'"avatar_url":"http:\\/\\/thirdqq.qlogo.cn\\/g?b=oidb&k=YPhqzYbLDibZ1GWLymWa5Uw&s=100&t=1598893744",' \
        b'"nick_name":"zzq","content":"\\u5367\\u69fd\\u5367\\u69fd\\u5367\\u69fd","openid":"","user_id":4,' \
        b'"user":{"id":4,"openid":"B68364D35797AF97B9C5889755D67FC8","nickname":"zzq",' \
        b'"avatar":"http:\\/\\/thirdqq.qlogo.cn\\/g?b=oidb&k=YPhqzYbLDibZ1GWLymWa5Uw&s=100&t=1598893744","os":" ",' \
        b'"client":" ","network_type":null,"posts_count_last_3_months":0,"posts_count":0,"mark_as_good_count":"",' \
        b'"mark_as_spam_count":0,"is_spam":false,"is_admin":null},"is_admin":true,"is_top":false,"is_good":false,' \
        b'"is_spam":false,"is_todo":false,"is_locked":false,"is_hidden":false,"is_notice":false,"is_liked":false,' \
        b'"is_abuse":false,"reply_count":0,"like_count":null,"images_count":0,"created_at":"2022-09-19 23:57:07",' \
        b'"time":"\\u73b0\\u5728","updated_at":"2022-09-19 23:57:07","last_reply_at":null,"images":[],"replies":[],' \
        b'"extra":[],"faq_id":0,"type":2,"replies_all":[],' \
        b'"post_url":"https:\\/\\/support.qq.com\\/product\\/377648\\/post\\/166360302733603118?","categories":[]}},' \
        b'"created_at":"2022-09-19T23:57:07+08:00","retry_count":0}'.decode(
        'utf-8')
    j = json.loads(a)
    print(json.dumps(j, indent=4))
    b: TxcHookEntity = TxcHookEntity.from_dict(j)
    print(b)