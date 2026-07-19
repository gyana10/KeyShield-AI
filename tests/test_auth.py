import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

TEST_USER = {
    "username": "testuser_pytest",
    "email": "testuser_pytest@keyshield.ai",
    "password": "StrongPassword123!"
}


def test_register_weak_password():
    res = client.post("/register", json={
        "username": "weakuser",
        "email": "weak@keyshield.ai",
        "password": "123"
    })
    assert res.status_code in [400, 422]


def test_register_and_login():
    # Register user
    reg_res = client.post("/register", json=TEST_USER)
    assert reg_res.status_code in [201, 400]

    # Login user
    login_res = client.post("/login", json={
        "email": TEST_USER["email"],
        "password": TEST_USER["password"]
    })
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


def test_invalid_jwt():
    res = client.get("/profile", headers={
        "Authorization": "Bearer invalid_token_xyz_123"
    })
    assert res.status_code == 401
