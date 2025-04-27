"""
Data Loader Utility
- Handles loading specific data fields from Parquet files.
"""

import pandas as pd
import os

def load_data_field(dataset_path: str, field: str) -> pd.DataFrame:
    """
    Load a specific data field from a Parquet file.

    Args:
        dataset_path (str): Path to the directory containing Parquet files.
        field (str): Name of the data field to load.

    Returns:
        pd.DataFrame: Loaded data field as a Pandas DataFrame.
    """
    filepath = os.path.join(dataset_path, f"{field}.parquet")
    return pd.read_parquet(filepath)