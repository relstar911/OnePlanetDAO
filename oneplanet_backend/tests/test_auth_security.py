from fastapi.testclient import TestClient
from oneplanet_backend.main import app

client = TestClient(app)


# --- JWT Login Success ---
def test_login_success():
    resp = client.post("/api/identity/login", json={"user_id": "authuser", "password": "pw"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()
    assert resp.json()["token_type"] == "bearer"


# --- JWT Login Failure (no user_id) ---
def test_login_failure_missing_user_id():
    resp = client.post("/api/identity/login", json={"password": "pw"})
    assert resp.status_code == 422
    errors = resp.json()["detail"]
    assert any(
        e.get("type") == "missing"
        and e.get("msg") == "Field required"
        and "user_id" in e.get("loc", [])
        for e in errors
    )


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
    print("NO TOKEN:", resp.status_code, resp.text)
    assert resp.status_code == 403
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
    print("INVALID TOKEN:", resp.status_code, resp.text)
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid or expired token"


# --- Auth Success: Access with Valid Token ---
def test_protected_endpoint_valid_token():
    login = client.post("/api/identity/login", json={"user_id": "authuser", "password": "pw"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
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
    assert resp.status_code == 200
    assert resp.json()["status"] == "success"
