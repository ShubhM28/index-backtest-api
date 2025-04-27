"""
Test Cases for BITA Mini Backtest API
- Covers both Equal and Optimized weighting strategies
- Covers Top-N and Value Threshold filtering methods
- Tests edge cases and invalid inputs
"""

import sys
import os

# Allow imports from parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ---------------------- TEST CASES ----------------------

# Test 1: Basic Equal Weighting + Top N + Quarterly
def test_equal_topn_quarterly():
    """
    Test equal weighting with Top-N filter and quarterly rebalancing.
    """
    response = client.post("/run-backtest", json={
        "dataset_path": "generated_data",
        "calendar": {
            "rule_type": "quarterly",
            "start_date": "2024-01-01"
        },
        "filter": {
            "filter_type": "top_n",
            "data_field": "prices",
            "N": 10
        },
        "weighting": {
            "method": "equal"
        }
    })
    assert response.status_code == 200
    assert "weights" in response.json()

# Test 2: Equal Weighting + Value Threshold + Quarterly
def test_equal_value_filter():
    """
    Test equal weighting with value threshold filter and quarterly calendar.
    """
    response = client.post("/run-backtest", json={
        "dataset_path": "generated_data",
        "calendar": {
            "rule_type": "quarterly",
            "start_date": "2023-01-01"
        },
        "filter": {
            "filter_type": "value_threshold",
            "data_field": "volume",
            "P": 50
        },
        "weighting": {
            "method": "equal"
        }
    })
    assert response.status_code == 200
    assert "weights" in response.json()

# Test 3: Optimized Weighting + Top N
def test_optimized_topn():
    """
    Test optimized weighting with Top-N filter and custom date.
    """
    response = client.post("/run-backtest", json={
        "dataset_path": "generated_data",
        "calendar": {
            "rule_type": "custom",
            "custom_dates": ["2024-06-30"]
        },
        "filter": {
            "filter_type": "top_n",
            "data_field": "market_capitalization",
            "N": 5
        },
        "weighting": {
            "method": "optimized",
            "data_field": "market_capitalization",
            "lb": 0.1,
            "ub": 0.5
        }
    })
    assert response.status_code == 200
    assert "weights" in response.json()

# Test 4: Optimized Weighting + Value Threshold
def test_optimized_threshold():
    """
    Test optimized weighting with value threshold filter.
    """
    response = client.post("/run-backtest", json={
        "dataset_path": "generated_data",
        "calendar": {
            "rule_type": "custom",
            "custom_dates": ["2024-09-30"]
        },
        "filter": {
            "filter_type": "value_threshold",
            "data_field": "adtv_3_month",
            "P": 30.0
        },
        "weighting": {
            "method": "optimized",
            "data_field": "adtv_3_month",
            "lb": 0.0005,
            "ub": 0.3
        }
    })
    assert response.status_code == 200
    assert "weights" in response.json()

# Test 5: Invalid Calendar Rule
def test_invalid_calendar():
    """
    Test invalid calendar rule input validation.
    """
    response = client.post("/run-backtest", json={
        "dataset_path": "generated_data",
        "calendar": {
            "rule_type": "invalid_rule"
        },
        "filter": {
            "filter_type": "top_n",
            "data_field": "prices",
            "N": 3
        },
        "weighting": {
            "method": "equal"
        }
    })
    assert response.status_code == 422  

# Test 6: No securities after filter (edge case)
def test_empty_filter_result():
    """
    Test when no securities pass the value threshold filter (edge case).
    """
    response = client.post("/run-backtest", json={
        "dataset_path": "generated_data",
        "calendar": {
            "rule_type": "custom",
            "custom_dates": ["2024-01-01"]
        },
        "filter": {
            "filter_type": "value_threshold",
            "data_field": "prices",
            "P": 1000  # Unrealistically high threshold to force empty result
        },
        "weighting": {
            "method": "equal"
        }
    })
    result = response.json()
    assert response.status_code == 200
    assert result["weights"] == {}