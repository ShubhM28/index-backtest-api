"""
Main Application Entrypoint
- Initializes FastAPI app
- Includes API routing
- Adds request logging middleware
"""

from fastapi import FastAPI, Request
from app.api import router
import logging

# Setup logger configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize FastAPI app with metadata
app = FastAPI(
    title="BITA Mini Backtest API",
    description="A lightweight backtesting engine built with FastAPI and Pandas.",
    version="1.0.0"
)

# Include application routers
app.include_router(router)

# Middleware to log all incoming HTTP requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware to log each incoming request's method and path.
    """
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    return response