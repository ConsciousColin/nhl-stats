import pandas as pd

from nhl_stats.nhl_api.client import get_player, get_teams
from nhl_stats.write_stats.write import write_data

def write_players_data(season:str):
    team_data = get_teams(season=season, expand="team.roster")
    player_data = []
    for team in team_data:
        for player in team['roster']['roster']:
            player_id = player['person']['id']
            player = get_player(player_id)
            player.pop('link')
            player_data.append(player)
    df = pd.json_normalize(player_data, sep='_')
    write_data(dataset_name="players", df=df, season=season)