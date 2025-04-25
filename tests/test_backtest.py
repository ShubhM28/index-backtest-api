from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_run_backtest():
    payload = {
        "dataset_path": "generated_data",
        "calendar": {
            "rule_type": "quarterly",
            "start_date": "2024-01-01"
        },
        "filter": {
            "filter_type": "top_n",
            "data_field": "market_capitalization",
            "N": 5
        },
        "weighting": {
            "method": "equal"
        }
    }

    response = client.post("/run-backtest", json=payload)
    assert response.status_code == 200
    json_resp = response.json()
    assert "execution_time" in json_resp
    assert "weights" in json_resp
    assert isinstance(json_resp["weights"], dict)