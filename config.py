from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class ReplyUserConfig:
    openid: str
    nickname: str
    avatar: str


@dataclass_json
@dataclass
class DatabaseConfig:
    username: str
    password: str
    host: str
    port: int
    database: str


@dataclass_json
@dataclass
class KiteBotConfig:
    proxy: str
    token: str
    chat_id: str


@dataclass_json
@dataclass
class Config:
    utc_tz_delta: int
    bot: KiteBotConfig
    reply_user: ReplyUserConfig
    database: DatabaseConfig


with open('config.json', encoding='utf-8') as f:
    current_config: Config = Config.from_json(f.read())

__all__ = [
    'current_config'
]
