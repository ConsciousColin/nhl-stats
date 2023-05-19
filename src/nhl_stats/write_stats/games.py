


from typing import Dict, List
import pandas as pd
from nhl_stats.nhl_api.client import get_schedule, get_game
from nhl_stats.write_stats.write import write_data


def _process_players_data(players: List[Dict], base_player_dict: Dict) -> List[Dict]:
    players_data = []
    for player_id, player in players.items():
        player_data = base_player_dict
        player_data['player_id'] = player['person']['id']
        if 'fullName' in player:
            player_data['player_name'] = player['person']['fullName']
        player_data['player_type'] = player['position']['type']
        player_data['player_position'] = player['position']['abbreviation']
        player_data['player_stats'] = player['stats']
        players_data.append(player_data)
    return players_data


def write_games_data(season:str):
    schedule_data = get_schedule(season=season)
    team_game_data = []
    player_game_data = []
    for schedule_date in schedule_data:
        for game in schedule_date['games']:
            home_players_data = {}
            away_players_data = {}
            game_id = game['gamePk']
            game = get_game(game_id)
            home_team = game['teams']['home']
            away_team = game['teams']['away']
            home_players_data['game_id'] = game_id
            away_players_data['game_id'] = game_id
            home_players_data['game_date'] = schedule_date['date']
            away_players_data['game_date'] = schedule_date['date']
            player_game_data.extend(
                _process_players_data(players=away_team['players'],
                                    base_player_dict=away_players_data)
                                    )
            player_game_data.extend(
                _process_players_data(players=home_team['players'], 
                                    base_player_dict=home_players_data)
                                    )

    team_df = pd.json_normalize(team_game_data, sep='_')
    player_df = pd.json_normalize(player_game_data, sep='_')
    write_data(dataset_name="nhl_team_game_stats", df=team_df, season=season)
    write_data(dataset_name="nhl_player_game_stats", df=player_df, season=season)
