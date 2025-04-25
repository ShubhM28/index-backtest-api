import pandas as pd
import numpy as np
import os

path = r"C:\Users\shubh\OneDrive\Desktop\bita-backtest-api\generated_data"
os.makedirs(path, exist_ok=True)

data_field_identifiers = [
    "market_capitalization",
    "prices",
    "volume",
    "adtv_3_month"
]

securities = list(map(str, range(1000)))
dates = pd.date_range("2020-01-01", "2025-01-22")

for data_field_identifier in data_field_identifiers:
    data = np.random.uniform(low=1, high=100, size=(len(dates), len(securities)))
    df = pd.DataFrame(data, index=dates, columns=securities)
    df.to_parquet(f"{path}/{data_field_identifier}.parquet")

