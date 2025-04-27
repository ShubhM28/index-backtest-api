"""
Utility Functions
- Handles revision date generation and data filtering operations.
"""

import pandas as pd
from datetime import datetime

def get_revision_dates(rule: dict) -> list:
    """
    Generate a list of revision dates based on the calendar rule.

    Args:
        rule (dict): Calendar rule specifying either 'custom' or 'quarterly'.

    Returns:
        list: List of revision dates as string in 'YYYY-MM-DD' format.
    """
    if rule["rule_type"] == "custom":
        return rule["custom_dates"]

    elif rule["rule_type"] == "quarterly":
        start = pd.Timestamp(rule["start_date"])
        end = pd.Timestamp("2025-01-22")
        return pd.date_range(start=start, end=end, freq='Q').strftime("%Y-%m-%d").tolist()

def apply_top_n_filter(df: pd.DataFrame, n: int) -> pd.Series:
    """
    Apply a Top-N filter on securities based on values.

    Args:
        df (pd.DataFrame): Series or single-row DataFrame of security values.
        n (int): Number of top securities to select.

    Returns:
        pd.Series: Filtered securities (top N by value).
    """
    return df.nlargest(n, keep='all')

def apply_value_threshold_filter(df: pd.DataFrame, p: float) -> pd.Series:
    """
    Filter securities whose values are above a specified threshold.

    Args:
        df (pd.DataFrame): Series or single-row DataFrame of security values.
        p (float): Threshold value.

    Returns:
        pd.Series: Filtered securities exceeding the threshold.
    """
    return df[df > p]