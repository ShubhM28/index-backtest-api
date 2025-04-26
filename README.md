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
# Step 1: Clone the repository
git clone <your-repo-url>
cd bita-backtest-api

# Step 2: Create and activate a virtual environment
python3.11 -m venv venv
# On Mac/Linux
source venv/bin/activate
# On Windows
venv\Scripts\activate

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Generate dummy data
python scripts/generate_data.py

# Step 5: Run the FastAPI server
uvicorn app.main:app --reload

## Test Coverage
The project includes extensive tests that verify the main functionalities of the backtest engine:

Test 1: Basic Equal Weighting + Top N + Quarterly
Tests basic flow where a portfolio is rebalanced quarterly using Top-N securities with equal weighting.
Expected: Returns non-empty weights equally distributed among selected securities.

Test 2: Equal Weighting + Value Threshold + Quarterly
Tests equal weighting when securities are selected based on a minimum value threshold from the dataset.
Expected: Returns non-empty equal weights among securities meeting the threshold.

Test 3: Optimized Weighting + Top N
Tests true optimization with Top-N securities under lower and upper bound constraints.
Expected: Returns optimized weights satisfying bounds and maximizing Dᵀw.

Test 4: Optimized Weighting + Value Threshold
Tests optimization after applying a value threshold filter resulting in a large set of securities.
Expected: Returns optimized weights if feasible, else safely returns empty if infeasible.

Test 5: Invalid Calendar Rule
Tests how the system handles invalid calendar rule input.
Expected: Returns HTTP 422 Unprocessable Entity error.

Test 6: No Securities After Filtering (Edge Case)
Tests the edge case where no securities pass the filter criteria.
Expected: Returns an empty weights dictionary gracefully without crashing.
