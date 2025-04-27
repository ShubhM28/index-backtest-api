"""
Dataset Generator
- Creates synthetic Parquet files for multiple financial fields.
- Each field contains randomly generated data for a range of dates and securities.
"""

import pandas as pd
import numpy as np
import os

# Define output path for generated data
path = r"C:\Users\shubh\OneDrive\Desktop\bita-backtest-api\generated_data"
os.makedirs(path, exist_ok=True)

# Data field identifiers to generate
data_field_identifiers = [
    "market_capitalization",
    "prices",
    "volume",
    "adtv_3_month"
]

# List of securities (string IDs)
securities = list(map(str, range(1000)))

# Date range for historical simulation
dates = pd.date_range("2020-01-01", "2025-01-22")

# Generate and save a Parquet file for each field
for data_field_identifier in data_field_identifiers:
    data = np.random.uniform(low=1, high=100, size=(len(dates), len(securities)))
    df = pd.DataFrame(data, index=dates, columns=securities)
    df.to_parquet(f"{path}/{data_field_identifier}.parquet")