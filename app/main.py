from fastapi import FastAPI,Request
from app.api import router
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="BITA Mini Backtest API",
    description="A lightweight backtesting engine built with FastAPI and Pandas.",
    version="1.0.0"
)
app.include_router(router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    return response