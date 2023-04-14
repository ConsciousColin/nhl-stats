from typing import Dict, List, Optional
from datetime import datetime
import requests
import json
import pandas as pd
from stringcase import snakecase

from nhl_stats.write_stats.seasons import get_latest_season_id


def _save_data(dataset_name: str, season:str, df: pd.DataFrame):
    data_uri = f'gs://nhl-data-snapshots/{dataset_name}/season={season}/data.parquet'
    df.to_parquet(data_uri, storage_options={"token": None})        


def write_team_stats_data(team_data: List[Dict], season:str):
    team_stats_relative = []
    team_stats_absolute = []
    for team in team_data:
        team_stats_relative_val = team['teamStats'][0]['splits'][0]['stat']
        team_stats_absolute_val = team['teamStats'][0]['splits'][1]['stat']
        team_stats_relative_val['team_id'] = team['id']
        team_stats_absolute_val['team_id'] = team['id']
        team_stats_relative.append(team_stats_relative_val)
        team_stats_absolute.append(team_stats_absolute_val)

    team_stats_abs_df = pd.DataFrame.from_dict(team_stats_absolute)
    team_stats_rel_df = pd.DataFrame.from_dict(team_stats_relative)
    _save_data(dataset_name="nhl_team_stats_absolute", df=team_stats_abs_df, season=season)
    _save_data(dataset_name="nhl_team_stats_relative", df=team_stats_rel_df, season=season)


def write_team_data(season: Optional[str]) -> None:
    if not season:
        season = get_latest_season_id()
    result = requests.get(f"https://statsapi.web.nhl.com/api/v1/teams?expand=team.stats&season={season}")
    data = json.loads(result.text)['teams']

    write_team_stats_data(data, season=season)
    df = pd.json_normalize(data, sep='_')
    df.drop(axis=1, 
            columns=['teamStats', 'officialSiteUrl', 'venue_timeZone_id', 'venue_timeZone_offset', 'link', 'venue_link', 
                    'venue_timeZone_tz', 'franchise_link', 'conference_link', 'division_link', 'franchise_franchiseId'], 
            inplace=True)
    column_map = {x: snakecase(x) for x in df.keys()}
    df.rename(columns=column_map, inplace=True)
    df.rename(columns={"id": "team_id"}, inplace=True)
    df.to_parquet('gs://nhl-data-snapshots/team_base.parquet', storage_options={"token": None})
    _save_data(dataset_name="nhl_teams", season=season, df=df)