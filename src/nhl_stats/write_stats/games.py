


from typing import Dict, List
import pandas as pd
from nhl_stats.nhl_api.client import get_schedule, get_game
from nhl_stats.write_stats.write import write_data


def _process_players_data(team_data: Dict, base_player_dict: Dict, is_away: bool) -> List[Dict]:
    players_data = []
    base_player_data = {}
    base_player_data.update(base_player_dict)
    base_player_data['team_id'] = team_data['team']['id']
    base_player_data['team_name'] = team_data['team']['name']
    base_player_data['is_away'] = is_away
    for player_key, player in team_data['players'].items():
        player_data = player['stats']
        player_data.update(base_player_data)
        player_data['player_id'] = player['person']['id']
        if 'fullName' in player:
            player_data['player_name'] = player['person']['fullName']
        player_data['player_type'] = player['position']['type']
        player_data['player_position'] = player['position']['abbreviation']
        players_data.append(player_data)
    return players_data


def _process_team_data(team: Dict, base_team_dict: Dict,  is_away: bool) -> Dict:
    team_data = {} 
    team_data.update(base_team_dict)
    team_data.update(team['teamStats']['teamSkaterStats'])
    team_data['team_id'] = team['team']['id']
    team_data['team_name'] = team['team']['name']
    team_data['is_away'] = is_away
    for coach in team['coaches']:
        if coach['position']['code'] == 'HC':
            team_data['coach_name'] = coach['person']['fullName']
    return team_data


def _process_boxscores(away_team: Dict, home_team: Dict, base_team_dict: Dict) -> Dict:
    boxscore_data = {}
    boxscore_data.update(base_team_dict)
    boxscore_data['away_team_id'] = away_team['team']['id']
    boxscore_data['away_team_name'] = away_team['team']['name']
    boxscore_data['away_team_goals'] = away_team['teamStats']['teamSkaterStats']['goals']
    boxscore_data['away_team_shots'] = away_team['teamStats']['teamSkaterStats']['shots']
    boxscore_data['home_team_id'] = home_team['team']['id']
    boxscore_data['home_team_name'] = home_team['team']['name']
    boxscore_data['home_team_goals'] = home_team['teamStats']['teamSkaterStats']['goals']
    boxscore_data['home_team_shots'] = home_team['teamStats']['teamSkaterStats']['shots']
    return boxscore_data


def write_games_data(season:str):
    schedule_data = get_schedule(season=season)
    team_game_data = []
    player_game_data = []
    game_boxscores = []
    for schedule_date in schedule_data:
        for game in schedule_date['games']:
            game_id = game['gamePk']
            game = get_game(game_id)
            home_team = game['teams']['home']
            away_team = game['teams']['away']
            base_game_data = {
                'game_id': game_id,
                'game_date': schedule_date['date']

            }
            player_game_data.extend(
                _process_players_data(team_data=away_team,
                                    base_player_dict=base_game_data,
                                    is_away=True)
                                    )
            player_game_data.extend(
                _process_players_data(team_data=home_team, 
                                    base_player_dict=base_game_data,
                                   is_away=False)
                                    )
            team_game_data.append(
                _process_team_data(team=away_team, 
                                   base_team_dict=base_game_data,
                                   is_away=True)
                                   )
            team_game_data.append(
                _process_team_data(team=home_team,
                                   base_team_dict=base_game_data,
                                   is_away=False)
                                   )
            game_boxscores.append(
                _process_boxscores(away_team=away_team,
                                   home_team=home_team,
                                   base_team_dict=base_game_data)
                                   )

    team_df = pd.json_normalize(team_game_data, sep='_')
    player_df = pd.json_normalize(player_game_data, sep='_')
    game_boxscores_df = pd.json_normalize(game_boxscores, sep='_')
    write_data(dataset_name="team_game_stats", df=team_df, season=season)
    write_data(dataset_name="player_game_stats", df=player_df, season=season)
    write_data(dataset_name="game_boxscores", df=game_boxscores_df, season=season)
