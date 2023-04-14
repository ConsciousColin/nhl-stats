
from functools import cache
import json
from typing import List

import requests


def get_seasons() -> List[dict]:
    result = requests.get("https://statsapi.web.nhl.com/api/v1/seasons")
    result = json.loads(result.text)["seasons"]
    return result

@cache
def get_latest_season_id():
    return get_seasons()[-1]['seasonId']