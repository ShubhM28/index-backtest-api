"""
Pydantic Models for Request and Response Validation
- Defines schemas for input and output data structures.
"""

from pydantic import BaseModel
from typing import List, Literal, Dict, Optional
from datetime import date

class CalendarRule(BaseModel):
    """
    Schema for defining rebalancing calendar rules.
    """
    rule_type: Literal['custom', 'quarterly']
    custom_dates: Optional[List[date]] = None  # Used when rule_type is custom
    start_date: Optional[date] = None           # Used when rule_type is quarterly

class FilterRule(BaseModel):
    """
    Schema for defining security filtering rules.
    """
    filter_type: Literal['top_n', 'value_threshold']
    data_field: str
    N: Optional[int] = None                     # For 'top_n' filtering
    P: Optional[float] = None                    # For 'value_threshold' filtering

class WeightingRule(BaseModel):
    """
    Schema for defining security weighting rules.
    """
    method: Literal['equal', 'optimized']
    data_field: Optional[str] = None             # Required for optimized method
    lb: Optional[float] = None                   # Lower bound for weights
    ub: Optional[float] = None                   # Upper bound for weights

class BacktestRequest(BaseModel):
    """
    Complete schema for a backtest API request.
    """
    dataset_path: str
    calendar: CalendarRule
    filter: FilterRule
    weighting: WeightingRule

class BacktestResponse(BaseModel):
    """
    Schema for the backtest API response.
    """
    execution_time: float
    weights: Dict[str, Dict[str, float]]