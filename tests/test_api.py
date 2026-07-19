import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

TEST_USER = {
    "username": "api_tester",
    "email": "api_tester@keyshield.ai",
    "password": "StrongPassword123!"
}

KEYSTROKE_PAYLOAD = {
    "holdTimes": [110.5, 95.2, 105.0, 100.8, 98.4],
    "flightTimes": [210.0, 180.5, 220.1, 195.3],
    "totalDuration": 3200.0,
    "backspaces": 0
}


@pytest.fixture
def auth_headers():
    client.post("/register", json=TEST_USER)
    res = client.post("/login", json={
        "email": TEST_USER["email"],
        "password": TEST_USER["password"]
    })
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_model_info_endpoint():
    res = client.get("/model-info")
    assert res.status_code == 200
    data = res.json()
    assert "architecture" in data
    assert "base_models" in data
    assert len(data["model_comparison"]) >= 4


def test_enrollment_workflow(auth_headers):
    # Sample 1
    res1 = client.post("/enroll", json=KEYSTROKE_PAYLOAD, headers=auth_headers)
    assert res1.status_code == 200
    assert res1.json()["sample_index"] >= 1

    # Sample 2
    res2 = client.post("/enroll", json=KEYSTROKE_PAYLOAD, headers=auth_headers)
    assert res2.status_code == 200

    # Sample 3
    res3 = client.post("/enroll", json=KEYSTROKE_PAYLOAD, headers=auth_headers)
    assert res3.status_code == 200
    assert res3.json()["enrollment_complete"] is True


def test_authentication_workflow(auth_headers):
    res = client.post("/authenticate", json=KEYSTROKE_PAYLOAD, headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["decision"] in ["GENUINE", "SUSPICIOUS"]
    assert data["risk"] in ["LOW", "MEDIUM", "HIGH"]
    assert "shap_explanation" in data


def test_profile_endpoint(auth_headers):
    res = client.get("/profile", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert "enrollment_complete" in data
    assert "hold_mean" in data


def test_history_endpoint(auth_headers):
    res = client.get("/history", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert "total" in data
    assert "logs" in data


def test_statistics_endpoint(auth_headers):
    res = client.get("/statistics", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert "total_authentications" in data
    assert "pass_rate" in data
