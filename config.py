from dataclasses import dataclass
from typing import Dict
import json

@dataclass
class KiteBotConfig:
    proxy: str
    token: str

    @staticmethod
    def fromJson(s: str):
        return KiteBotConfig(**json.loads(s))