from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class KiteBotConfig:
    proxy: str
    token: str
    chat_id: str
