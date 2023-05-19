import pandas as pd
from nhl_stats.nhl_api.client import get_seasons
from nhl_stats.write_stats.write import write_data


def write_seasons_data():
    seasons = get_seasons()
    df = pd.json_normalize(seasons, sep='_')
    write_data(dataset_name="nhl_seasons", df=df, season=None)

