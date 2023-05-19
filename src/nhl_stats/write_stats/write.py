import pandas as pd
import os

GCS_BUCKET = os.getenv("NHL_DATA_GCS_BUCKET")

def write_data(dataset_name: str, season:str, df: pd.DataFrame):
    data_uri = f'gs://{GCS_BUCKET}/{dataset_name}/season={season}/data.parquet'
    df.to_parquet(data_uri, storage_options={"token": None}) 