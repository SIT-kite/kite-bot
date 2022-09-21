from datetime import *
from config import current_config


def utc_2_local_tz(t: datetime):
    return t.astimezone(timezone(timedelta(
        hours=current_config.utc_tz_delta
    )))
