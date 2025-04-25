import pandas as pd
from datetime import datetime

def get_revision_dates(rule: dict) -> list:
    if rule["rule_type"] == "custom":
        return rule["custom_dates"]
    
    elif rule["rule_type"] == "quarterly":
        start = pd.Timestamp(rule["start_date"])
        end = pd.Timestamp("2025-01-22")
        return pd.date_range(start=start, end=end, freq='Q').strftime("%Y-%m-%d").tolist()

def apply_top_n_filter(df: pd.DataFrame, n: int) -> pd.Series:
    return df.nlargest(n, keep='all')

def apply_value_threshold_filter(df: pd.DataFrame, p: float) -> pd.Series:
    return df[df > p]