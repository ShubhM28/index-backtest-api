# BITA Mini Backtest API

A mini backtesting engine for running portfolio simulations using customizable rules (calendar, filters, weights) built with FastAPI, Pandas, and Pydantic.

## Features

- Custom or quarterly portfolio rebalancing dates
- Two filtering strategies:
  - Top N by data field
  - Value threshold filter
- Two weighting strategies:
  - Equal weight
  - Optimized weights within bounds
- Reads from Parquet files
- FastAPI + Swagger docs
- Lightweight, testable, and extendable

## Tech Stack

- Python 3.11
- FastAPI
- Pandas, NumPy
- PyArrow
- Pydantic
- Pytest

## How to Run

1. Clone the repo
2. Create and activate a virtual environment

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python scripts/generate_data.py
uvicorn app.main:app --reload
Go To --> http://localhost:8000/docs

