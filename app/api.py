from fastapi import APIRouter
from app.models import BacktestRequest, BacktestResponse
from app.backtest_engine import run_backtest

router = APIRouter()

@router.post("/run-backtest", response_model=BacktestResponse)
def run_backtest_endpoint(req: BacktestRequest):
    return run_backtest(req.dict())