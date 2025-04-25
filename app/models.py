from pydantic import BaseModel
from typing import List, Literal, Dict, Optional
from datetime import date

class CalendarRule(BaseModel):
    rule_type: Literal['custom', 'quarterly']
    custom_dates: Optional[List[date]] = None
    start_date: Optional[date] = None  # for quarterly

class FilterRule(BaseModel):
    filter_type: Literal['top_n', 'value_threshold']
    data_field: str
    N: Optional[int] = None
    P: Optional[float] = None

class WeightingRule(BaseModel):
    method: Literal['equal', 'optimized']
    data_field: Optional[str] = None
    lb: Optional[float] = None
    ub: Optional[float] = None

class BacktestRequest(BaseModel):
    dataset_path: str
    calendar: CalendarRule
    filter: FilterRule
    weighting: WeightingRule

class BacktestResponse(BaseModel):
    execution_time: float
    weights: Dict[str, Dict[str, float]]