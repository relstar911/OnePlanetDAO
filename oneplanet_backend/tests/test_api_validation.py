import pytest
from fastapi.testclient import TestClient
from oneplanet_backend.main import app
from oneplanet_backend.core.db import engine
from sqlmodel import SQLModel

@pytest.fixture(autouse=True, scope="session")
def create_test_tables():
    SQLModel.metadata.create_all(engine)

client = TestClient(app)

# --- Voting Success Test ---
def test_vote_success():
    data = {
        "user_id": "user_ok",
        "proposal_id": "prop_ok",
        "vote_weights": {"choiceA": 1, "choiceB": 2},
        "proof": "valid-proof"
    }
    resp = client.post("/api/governance/vote", json=data)
    assert resp.status_code == 200
    assert resp.json()["status"] == "success"

# --- Voting Validation Tests ---
def test_vote_missing_fields():
    resp = client.post("/api/governance/vote", json={})
    assert resp.status_code == 422
    # Bei komplett leerem Body kommt ein generischer Fehler von FastAPI/Pydantic
    # Daher keine spezifische Message prüfen

def test_vote_negative_weights():
    data = {
        "user_id": "user1",
        "proposal_id": "prop1",
        "vote_weights": {"choiceA": -1},
        "proof": "abc"
    }
    resp = client.post("/api/governance/vote", json=data)
    assert resp.status_code == 422
    assert "vote_weights" in resp.text

def test_vote_empty_proof():
    data = {
        "user_id": "user1",
        "proposal_id": "prop1",
        "vote_weights": {"choiceA": 1},
        "proof": ""
    }
    resp = client.post("/api/governance/vote", json=data)
    assert resp.status_code == 422
    # Bei leerem String wird Pflichtfeld-Fehler ausgegeben

# --- ProofRequest Success Test ---
def test_proof_request_success():
    data = {
        "user_id": "user_ok",
        "proof_type": "voting",
        "public_signals": ["1", "2", "3"],
        "external_nullifier": "null_ok"
    }
    resp = client.post("/api/identity/proof-request", json=data)
    assert resp.status_code == 200
    assert resp.json()["status"] == "success"

# --- ProofRequest Validation Tests ---
def test_proof_request_invalid_type():
    data = {
        "user_id": "user1",
        "proof_type": "invalid",
        "public_signals": [1,2],
        "external_nullifier": "n"
    }
    resp = client.post("/api/identity/proof-request", json=data)
    assert resp.status_code == 422
    assert "proof_type" in resp.text

def test_proof_request_empty_signals():
    data = {
        "user_id": "user1",
        "proof_type": "onboarding",
        "public_signals": [],
        "external_nullifier": "n"
    }
    resp = client.post("/api/identity/proof-request", json=data)
    assert resp.status_code == 422
    assert "public_signals" in resp.text

# --- KPI Success Test ---
def test_kpi_success():
    data = {
        "region": "EU",
        "onRampSuccess": 2,
        "accessibilityScore": 0.7,
        "privacyShieldOptIn": 1,
        "empowermentKPI": 5
    }
    resp = client.post("/api/reporting/kpis", json=data)
    assert resp.status_code == 200
    assert resp.json()["region"] == "EU"

# --- KPI Validation Tests ---
def test_kpi_invalid_accessibility():
    data = {
        "region": "EU",
        "onRampSuccess": 1,
        "accessibilityScore": 2.0,
        "privacyShieldOptIn": 1,
        "empowermentKPI": 1
    }
    resp = client.post("/api/reporting/kpis", json=data)
    assert resp.status_code == 422
    assert "accessibilityScore" in resp.text

# --- Alert Success Test ---
def test_alert_success():
    data = {
        "epoch": 1,
        "msi": 0.5,
        "vei": 0.5,
        "collusion": "none",
        "status": "ok",
        "alert": "test alert"
    }
    resp = client.post("/api/tokenomics/alerts", json=data)
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

# --- Alert Validation Tests ---
def test_alert_invalid_msi():
    data = {
        "epoch": 1,
        "msi": 1.5,
        "vei": 0.5,
        "collusion": "none",
        "status": "ok",
        "alert": "test"
    }
    resp = client.post("/api/tokenomics/alerts", json=data)
    assert resp.status_code == 422
    assert "msi" in resp.text
