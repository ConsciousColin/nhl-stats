from dataclasses import dataclass
from functools import cache
from typing import Dict, List, Optional
import requests
import json

NHL_STATS_API_URL = "https://statsapi.web.nhl.com/api/v1/"


def base_get_call(api_suffix: str, season: Optional[str], extra_args: Optional[str]) -> requests.Response:
    if not season:
        season = get_latest_season_id()
    call_url = f"{NHL_STATS_API_URL}{api_suffix}?season={season}"
    if extra_args:
        call_url += extra_args
    return requests.get(call_url)


def get_teams(season: Optional[str], expand: Optional[str]) -> Dict:
    result = base_get_call(api_suffix="teams", season=season, 
                           extra_args=f"&expand={expand}")
    return json.loads(result.text)['teams']


def get_player(player_id: str) -> Dict:
    result = base_get_call(api_suffix=f"people/{player_id}", season=None, 
                           extra_args=None)
    return json.loads(result.text)['people'][0]


def get_player_stats(player_id: str, stats: str, season: Optional[str]) -> Dict:
    result = base_get_call(api_suffix=f"people/{player_id}/stats", season=season, 
                           extra_args=f"stats={stats}")
    return json.loads(result.text)['people']


def get_schedule(season: str) -> Dict:
    result = base_get_call(api_suffix="schedule", season=season, 
                           extra_args="&expand=schedule.lineScore")
    return json.loads(result.text)['dates']


def get_game(game_id: str) -> Dict:
    result = base_get_call(api_suffix=f"game/{game_id}/boxscore", season=None, 
                           extra_args=None)
    return json.loads(result.text)


def get_seasons() -> List[dict]:
    result = requests.get(f"{NHL_STATS_API_URL}seasons")
    result = json.loads(result.text)["seasons"]
    return result


@cache
def get_latest_season_id():
    result = requests.get(f"{NHL_STATS_API_URL}seasons/current")
    result = json.loads(result.text)["seasons"][0]
    return result["seasonId"]