import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

SAMPLE_RAW_EVENTS = [
    {"key": "T", "type": "keydown", "time": 0.0},
    {"key": "T", "type": "keyup", "time": 110.0},
    {"key": "h", "type": "keydown", "time": 140.0},
    {"key": "h", "type": "keyup", "time": 250.0},
    {"key": "e", "type": "keydown", "time": 290.0},
    {"key": "e", "type": "keyup", "time": 400.0}
]

ENROLLMENT_PAYLOAD = {
    "samples": [SAMPLE_RAW_EVENTS] * 5
}

VERIFICATION_PAYLOAD = {
    "events": SAMPLE_RAW_EVENTS
}


def test_model_info_endpoint():
    res = client.get("/model-info")
    assert res.status_code == 200
    data = res.json()
    assert "model_comparison" in data


def test_enrollment_workflow():
    res = client.post("/enroll", json=ENROLLMENT_PAYLOAD)
    assert res.status_code == 200
    data = res.json()
    assert data["enrollment_complete"] is True
    assert data["total_samples"] == 5


def test_authentication_workflow():
    res = client.post("/authenticate", json=VERIFICATION_PAYLOAD)
    assert res.status_code == 200
    data = res.json()
    assert data["decision"] in ["GENUINE", "SUSPICIOUS"]
    assert data["risk"] in ["LOW", "MEDIUM", "HIGH"]
    assert "text_explanation" in data
    assert "isolation_forest_result" in data
    assert "stacking_probability" in data


def test_dashboard_endpoints():
    res_prof = client.get("/profile")
    assert res_prof.status_code == 200

    res_hist = client.get("/history")
    assert res_hist.status_code == 200

    res_stats = client.get("/statistics")
    assert res_stats.status_code == 200
