from fastapi import APIRouter, HTTPException
from app.models import BacktestRequest, BacktestResponse
from app.backtest_engine import run_backtest

router = APIRouter()

@router.post(
    "/run-backtest",
    response_model=BacktestResponse,
    summary="Initiate a backtesting process.",
    description=(
        "Accepts a BacktestRequest payload containing the necessary parameters "
        "to execute a backtest and returns a BacktestResponse with the results."
    ),
)
def run_backtest_endpoint(req: BacktestRequest):
    """
    Endpoint to trigger the backtesting engine.

    Args:
        req (BacktestRequest): The input data for the backtest, including strategy parameters,
                                 historical data range, and other relevant configurations.

    Returns:
        BacktestResponse: A JSON response containing the results of the backtest execution,
                          such as performance metrics, trade details, and summary statistics.
    """
    # Log the incoming backtest request for debugging and monitoring purposes.
    print(f"Received backtest request: {req.dict()}")
    try:
        # Delegate the actual backtesting logic to the dedicated backtest engine.
        results = run_backtest(req.dict())
        return results
    except Exception as e:
        # Handle any potential exceptions during the backtest execution gracefully.
        print(f"Error during backtest: {e}")
        # Consider returning a more specific error response to the client.
        raise HTTPException(status_code=500, detail=f"Backtest execution failed: {e}")

@router.get(
    "/health",
    summary="Health check endpoint.",
    description="Simple endpoint to verify the API's availability and basic functionality.",
)
def health_check():
    """
    Basic health check endpoint.

    Returns:
        dict: A JSON response indicating the service's health status.
              Currently, it returns {"status": "ok"} if the service is running.
    """
    return {"status": "ok"}