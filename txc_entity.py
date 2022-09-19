from dataclasses import dataclass
from datetime import datetime
import enum
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
    type: EventType
    created_at: datetime
    payload: Union[PostEntity, ReplyEntity]

    @staticmethod
    def fromDict(dic: Dict[str, Any]):
        if dic['type'] == 'post.created':
            payload = PostEntity.fromDict(dic['payload'])
        if dic['type'] == 'post.updated':
            payload = PostEntity.fromDict(dic['payload'])
        return HookEntity(
            id=dic['id'],
            payload=payload
        )
