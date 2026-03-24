import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from oneplanet_backend.core.db import engine
from oneplanet_backend.core.limiter import limiter
from oneplanet_backend.main import app

limiter.enabled = False

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_test_tables():
    SQLModel.metadata.create_all(engine)
    from sqlmodel import Session

    with Session(engine) as session:
        for table in reversed(SQLModel.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()


def _register_and_login(user_id="authuser", password="testpass1234"):
    """Helper: register user then login, return token."""
    client.post(
        "/api/identity/register",
        json={"user_id": user_id, "password": password},
    )
    resp = client.post(
        "/api/identity/login",
        json={"user_id": user_id, "password": password},
    )
    return resp


# --- Registration ---
def test_register_success():
    resp = client.post(
        "/api/identity/register",
        json={"user_id": "newuser", "password": "pass1234"},
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()
    assert resp.json()["user_id"] == "newuser"


def test_register_duplicate():
    client.post(
        "/api/identity/register",
        json={"user_id": "dupuser", "password": "pass1234"},
    )
    resp = client.post(
        "/api/identity/register",
        json={"user_id": "dupuser", "password": "pass1234"},
    )
    assert resp.status_code == 409


def test_register_short_password():
    resp = client.post(
        "/api/identity/register",
        json={"user_id": "shortpw", "password": "ab"},
    )
    assert resp.status_code == 400
    assert "4 characters" in resp.json()["detail"]


# --- JWT Login Success ---
def test_login_success():
    _register_and_login("loginuser", "testpass1234")
    resp = client.post(
        "/api/identity/login",
        json={"user_id": "loginuser", "password": "testpass1234"},
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()
    assert resp.json()["token_type"] == "bearer"


# --- JWT Login Failure (wrong password) ---
def test_login_wrong_password():
    _register_and_login("wrongpw_user", "correctpass")
    resp = client.post(
        "/api/identity/login",
        json={"user_id": "wrongpw_user", "password": "wrongpass"},
    )
    assert resp.status_code == 401
    assert "Invalid credentials" in resp.json()["detail"]


# --- JWT Login Failure (no user_id) ---
def test_login_failure_missing_user_id():
    resp = client.post("/api/identity/login", json={"password": "pw"})
    assert resp.status_code == 422


# --- JWT Login Failure (user not registered) ---
def test_login_user_not_found():
    resp = client.post(
        "/api/identity/login",
        json={"user_id": "ghost", "password": "pass1234"},
    )
    assert resp.status_code == 401


# --- Auth Required: Access without Token ---
def test_protected_endpoint_no_token():
    resp = client.post(
        "/api/identity/proof-request",
        json={
            "user_id": "authuser",
            "proof_type": "onboarding",
            "public_signals": ["sig"],
            "external_nullifier": "null",
        },
    )
    assert resp.status_code in (401, 403)
    assert resp.json()["detail"] == "Not authenticated"


# --- Auth Required: Access with Invalid Token ---
def test_protected_endpoint_invalid_token():
    headers = {"Authorization": "Bearer invalidtoken"}
    resp = client.post(
        "/api/identity/proof-request",
        json={
            "user_id": "authuser",
            "proof_type": "onboarding",
            "public_signals": ["sig"],
            "external_nullifier": "null",
        },
        headers=headers,
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid or expired token"


# --- Auth Success: Access with Valid Token ---
def test_protected_endpoint_valid_token():
    login = _register_and_login("authuser2", "testpass1234")
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.post(
        "/api/identity/proof-request",
        json={
            "user_id": "authuser2",
            "proof_type": "onboarding",
            "public_signals": ["sig"],
            "external_nullifier": "null",
        },
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "success"
