import pandas as pd
import os

def load_data_field(dataset_path: str, field: str) -> pd.DataFrame:
    filepath = os.path.join(dataset_path, f"{field}.parquet")
    return pd.read_parquet(filepath)