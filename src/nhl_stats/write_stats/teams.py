from typing import Dict, List, Optional
import pandas as pd
from stringcase import snakecase
from nhl_stats.nhl_api.client import get_teams

from nhl_stats.write_stats.write import write_data      


def write_team_stats_data(season:str):
    team_data = get_teams(season=season, expand="team.stats")
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
    write_data(dataset_name="nhl_team_stats_absolute", df=team_stats_abs_df, season=season)
    write_data(dataset_name="nhl_team_stats_relative", df=team_stats_rel_df, season=season)


def write_team_roster_data(season:str):
    team_data = get_teams(season=season, expand="team.roster")
    team_rosters = []
    for team in team_data:
        roster = []
        for player in team['roster']['roster']:
            player_data = {}
            player_data['team_id'] = team['id']
            player_data['team_name'] = team['teamName']
            player_data['player_id'] = player['person']['id']
            player_data['player_name'] = player['person']['fullName']
            if 'jerseyNumber' in player:
                player_data['jersey_num'] = player['jerseyNumber']
            player_data['position_code'] = player['position']['code']
            player_data['position_name'] = player['position']['name']
            player_data['position_type'] = player['position']['type']
            roster.append(player_data)
        team_rosters.extend(roster)

    team_rosters_df = pd.DataFrame.from_dict(team_rosters)
    write_data(dataset_name="nhl_team_rosters", df=team_rosters_df, season=season)


def write_team_base_data(season: str):
    data = get_teams(season=season, expand=None)
    df = pd.json_normalize(data, sep='_')
    df.drop(axis=1, 
            columns=['officialSiteUrl', 'venue_timeZone_id', 'venue_timeZone_offset', 'link', 'venue_link', 
                    'venue_timeZone_tz', 'franchise_link', 'conference_link', 'division_link', 'franchise_franchiseId'], 
            inplace=True)
    column_map = {x: snakecase(x) for x in df.keys()}
    df.rename(columns=column_map, inplace=True)
    df.rename(columns={"id": "team_id"}, inplace=True)
    write_data(dataset_name="nhl_teams", season=season, df=df)

def write_team_data(season: Optional[str]) -> None:
    write_team_base_data(season)
    write_team_stats_data(season=season)
    write_team_roster_data(season=season)
