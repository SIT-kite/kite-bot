from dataclasses import dataclass
from datetime import datetime
import enum
import json
from typing import *



class EventType(enum.Enum):
    post_created = 'post.created'
    post_updated = 'post.updated'
    reply_created = 'reply.created'
    reply_updated = 'reply.updated'

@dataclass
class PostEntity:
    content: str

    @staticmethod
    def fromDict(dic: Dict[str, Any]):
        return PostEntity(
            content=dic['content'],
        )


@dataclass
class ReplyEntity:
    content: str
    
    @staticmethod
    def fromDict(dic: Dict[str, Any]):
        return ReplyEntity(
            content=dic['content'],
        )


@dataclass
class HookEntity:
    id: str
    # type: EventType
    # created_at: datetime
    payload: Union[PostEntity, ReplyEntity]

    @staticmethod
    def fromDict(dic: Dict[str, Any]):
        if dic['type'] == 'post.created':
            payload = PostEntity.fromDict(dic['payload']['post'])
        if dic['type'] == 'post.updated':
            payload = PostEntity.fromDict(dic['payload']['post'])
        return HookEntity(
            id=dic['id'],
            payload=payload
        )
if __name__ == '__main__':
    a = b'{"id":"36601f779a56dfde511045ade752b837","type":"post.created","payload":{"post":{"id":"166360302733603118","product_id":377648,"has_admin_reply":false,"avatar_url":"http:\\/\\/thirdqq.qlogo.cn\\/g?b=oidb&k=YPhqzYbLDibZ1GWLymWa5Uw&s=100&t=1598893744","nick_name":"zzq","content":"\\u5367\\u69fd\\u5367\\u69fd\\u5367\\u69fd","openid":"","user_id":4,"user":{"id":4,"openid":"B68364D35797AF97B9C5889755D67FC8","nickname":"zzq","avatar":"http:\\/\\/thirdqq.qlogo.cn\\/g?b=oidb&k=YPhqzYbLDibZ1GWLymWa5Uw&s=100&t=1598893744","os":" ","client":" ","network_type":null,"posts_count_last_3_months":0,"posts_count":0,"mark_as_good_count":"","mark_as_spam_count":0,"is_spam":false,"is_admin":null},"is_admin":true,"is_top":false,"is_good":false,"is_spam":false,"is_todo":false,"is_locked":false,"is_hidden":false,"is_notice":false,"is_liked":false,"is_abuse":false,"reply_count":0,"like_count":null,"images_count":0,"created_at":"2022-09-19 23:57:07","time":"\\u73b0\\u5728","updated_at":"2022-09-19 23:57:07","last_reply_at":null,"images":[],"replies":[],"extra":[],"faq_id":0,"type":2,"replies_all":[],"post_url":"https:\\/\\/support.qq.com\\/product\\/377648\\/post\\/166360302733603118?","categories":[]}},"created_at":"2022-09-19T23:57:07+08:00","retry_count":0}'.decode('utf-8')
    b = HookEntity.fromDict(json.loads(a))
    print(b)