import pandas as pd
import os

GCS_BUCKET = os.getenv("NHL_DATA_GCS_BUCKET")

def write_data(dataset_name: str, season:str, df: pd.DataFrame):
    season_attr = f"/season={season}" if season else ""
    data_uri = f'gs://{GCS_BUCKET}/{dataset_name}{season_attr}/data.parquet'
    df.to_parquet(data_uri, storage_options={"token": None}) 