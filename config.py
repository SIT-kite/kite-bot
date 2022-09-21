from dataclasses import dataclass
from dataclasses_json import dataclass_json
import yaml
import os.path


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


if os.path.isfile('config.yaml'):
    with open('config.yaml', encoding='utf-8') as f:
        current_config: Config = Config.from_dict(yaml.full_load((f.read())))
elif os.path.isfile('config.json'):
    with open('config.json', encoding='utf-8') as f:
        current_config: Config = Config.from_json(f.read())
else:
    s = 'Not found config file config.yaml or config.json'
    print(f'ERROR: {s}')
    raise s

__all__ = [
    'current_config'
]
