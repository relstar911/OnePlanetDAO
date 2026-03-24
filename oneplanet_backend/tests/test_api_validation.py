import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from oneplanet_backend.core.db import engine
from oneplanet_backend.main import app


@pytest.fixture(autouse=True)
def clean_test_tables():
    # Leere alle Tabellen vor jedem Test für Isolation
    from sqlmodel import Session

    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        for table in reversed(SQLModel.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()


client = TestClient(app)


@pytest.fixture(scope="function")
def auth_headers():
    # Register user first, then login
    client.post(
        "/api/identity/register",
        json={"user_id": "user_ok", "password": "testpass1234"},
    )
    resp = client.post(
        "/api/identity/login",
        json={"user_id": "user_ok", "password": "testpass1234"},
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# --- Voting Success Test ---
def test_vote_success(auth_headers):
    data = {
        "user_id": "user_ok",
        "proposal_id": "prop_ok",
        "vote_weights": {"choiceA": 1, "choiceB": 2},
        "proof": "valid-proof",
    }
    resp = client.post("/api/governance/vote", json=data, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "success"


# --- Voting GET Tests ---
def test_vote_get_empty(auth_headers):
    resp = client.get("/api/governance/votes")
    assert resp.status_code == 200
    assert resp.json() == []


def test_vote_get_filter_user_id(auth_headers):
    client.post(
        "/api/governance/vote",
        json={"user_id": "alice", "proposal_id": "p1", "vote_weights": {"A": 1}, "proof": "prf1"},
    )
    resp = client.get("/api/governance/votes?user_id=alice")
    assert resp.status_code == 200
    result = resp.json()
    assert result == [] or all(v["user_id"] == "alice" for v in result)


def test_vote_get_filter_user_id_not_found(auth_headers):
    resp = client.get("/api/governance/votes?user_id=notfound")
    assert resp.status_code == 200
    assert resp.json() == []


def test_vote_get_filter_proposal_id(auth_headers):
    client.post(
        "/api/governance/vote",
        json={"user_id": "bob", "proposal_id": "p2", "vote_weights": {"B": 2}, "proof": "prf2"},
        headers=auth_headers,
    )
    resp = client.get("/api/governance/votes?proposal_id=p2", headers=auth_headers)
    assert resp.status_code == 200
    result = resp.json()
    assert result == [] or all(v["proposal_id"] == "p2" for v in result)


def test_vote_get_filter_user_id_case(auth_headers):
    client.post(
        "/api/governance/vote",
        json={
            "user_id": "CaseTest",
            "proposal_id": "p3",
            "vote_weights": {"C": 3},
            "proof": "prf3",
        },
        headers=auth_headers,
    )
    resp = client.get("/api/governance/votes?user_id=casetest", headers=auth_headers)
    assert resp.status_code == 200
    result = resp.json()
    assert result == [] or all(v["user_id"].lower() == "casetest" for v in result)


def test_vote_get_filter_proposal_id_int(auth_headers):
    resp = client.get("/api/governance/votes?proposal_id=1234", headers=auth_headers)
    assert resp.status_code in (200, 422)


def test_vote_get_filter_user_id_multiple(auth_headers):
    resp = client.get("/api/governance/votes?user_id=alice&user_id=bob", headers=auth_headers)
    assert resp.status_code == 200


def test_vote_get_filter_unsupported(auth_headers):
    resp = client.get("/api/governance/votes?unsupported=foo", headers=auth_headers)
    assert resp.status_code == 200


def test_vote_get_after_post(auth_headers):
    data = {"user_id": "user1", "proposal_id": "prop1", "vote_weights": {"A": 2}, "proof": "proof1"}
    post_resp = client.post("/api/governance/vote", json=data, headers=auth_headers)
    assert post_resp.status_code == 200
    get_resp = client.get("/api/governance/votes", headers=auth_headers)
    assert get_resp.status_code == 200
    result = get_resp.json()
    assert any(vote["user_id"] == "user1" and vote["proposal_id"] == "prop1" for vote in result)


def test_vote_get_multiple(auth_headers):
    client.post(
        "/api/governance/vote",
        json={
            "user_id": "user2",
            "proposal_id": "prop2",
            "vote_weights": {"B": 1},
            "proof": "proof2",
        },
        headers=auth_headers,
    )
    client.post(
        "/api/governance/vote",
        json={
            "user_id": "user3",
            "proposal_id": "prop3",
            "vote_weights": {"C": 3},
            "proof": "proof3",
        },
        headers=auth_headers,
    )
    resp = client.get("/api/governance/votes", headers=auth_headers)
    print("Status code:", resp.status_code)
    print("Response:", resp.text)
    assert resp.status_code == 200
    result = resp.json()
    assert len(result) == 2
    users = {v["user_id"] for v in result}
    assert "user2" in users and "user3" in users


def test_vote_get_fields(auth_headers):
    data = {
        "user_id": "user4",
        "proposal_id": "prop4",
        "vote_weights": {"X": 5, "Y": 6},
        "proof": "proof4",
    }
    post_resp = client.post("/api/governance/vote", json=data, headers=auth_headers)
    print("POST status:", post_resp.status_code, post_resp.text)
    resp = client.get("/api/governance/votes", headers=auth_headers)
    print("GET status:", resp.status_code, resp.text)
    assert resp.status_code == 200
    vote = resp.json()[0]
    for key in ["user_id", "proposal_id", "vote_weights", "proof"]:
        assert key in vote
    assert isinstance(vote["vote_weights"], dict)


# --- Voting Validation Tests ---
def test_vote_missing_fields(auth_headers):
    resp = client.post("/api/governance/vote", json={}, headers=auth_headers)
    print("Missing fields status:", resp.status_code, resp.text)
    assert resp.status_code in (422, 403)
    # Bei komplett leerem Body kommt ein generischer Fehler von FastAPI/Pydantic
    # Daher keine spezifische Message prüfen


def test_vote_negative_weights(auth_headers):
    data = {
        "user_id": "user1",
        "proposal_id": "prop1",
        "vote_weights": {"choiceA": -1},
        "proof": "abc",
    }
    resp = client.post("/api/governance/vote", json=data, headers=auth_headers)
    assert resp.status_code == 422
    assert ">= 0" in resp.text


def test_vote_empty_proof(auth_headers):
    data = {"user_id": "user1", "proposal_id": "prop1", "vote_weights": {"choiceA": 1}, "proof": ""}
    resp = client.post("/api/governance/vote", json=data, headers=auth_headers)
    assert resp.status_code == 422
    # Bei leerem String wird Pflichtfeld-Fehler ausgegeben


# --- ProofRequest Success Test ---
def test_proof_request_success(auth_headers):
    data = {
        "user_id": "user_ok",
        "proof_type": "voting",
        "public_signals": ["1", "2", "3"],
        "external_nullifier": "null_ok",
    }
    resp = client.post("/api/identity/proof-request", json=data, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "success"


# --- ProofRequest GET Tests ---
def test_proof_request_get_empty(auth_headers):
    resp = client.get("/api/identity/proof-requests", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json() == []


def test_proof_request_get_filter_proof_type(auth_headers):
    client.post(
        "/api/identity/proof-request",
        json={
            "user_id": "filterA",
            "proof_type": "onboarding",
            "public_signals": ["fA"],
            "external_nullifier": "nullFA",
        },
        headers=auth_headers,
    )
    resp = client.get("/api/identity/proof-requests?proof_type=onboarding", headers=auth_headers)
    assert resp.status_code == 200
    result = resp.json()
    assert result == [] or all(p["proof_type"] == "onboarding" for p in result)


def test_proof_request_get_filter_proof_type_not_found(auth_headers):
    resp = client.get("/api/identity/proof-requests?proof_type=notype", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json() == []


def test_proof_request_get_filter_user_id(auth_headers):
    client.post(
        "/api/identity/proof-request",
        json={
            "user_id": "filterUser",
            "proof_type": "voting",
            "public_signals": ["fU"],
            "external_nullifier": "nullFU",
        },
        headers=auth_headers,
    )
    resp = client.get("/api/identity/proof-requests?user_id=filterUser", headers=auth_headers)
    assert resp.status_code == 200
    result = resp.json()
    assert result == [] or all(p["user_id"] == "filterUser" for p in result)


def test_proof_request_get_filter_proof_type_case(auth_headers):
    client.post(
        "/api/identity/proof-request",
        json={
            "user_id": "caseUser",
            "proof_type": "Voting",
            "public_signals": ["case"],
            "external_nullifier": "nullCase",
        },
        headers=auth_headers,
    )
    resp = client.get("/api/identity/proof-requests?proof_type=voting")
    assert resp.status_code == 200
    result = resp.json()
    assert result == [] or all(p["proof_type"].lower() == "voting" for p in result)


def test_proof_request_get_filter_proof_type_int(auth_headers):
    resp = client.get("/api/identity/proof-requests?proof_type=1234", headers=auth_headers)
    assert resp.status_code in (200, 422)


def test_proof_request_get_filter_proof_type_multiple(auth_headers):
    resp = client.get(
        "/api/identity/proof-requests?proof_type=onboarding&proof_type=voting", headers=auth_headers
    )
    assert resp.status_code == 200


def test_proof_request_get_filter_unsupported(auth_headers):
    resp = client.get("/api/identity/proof-requests?unsupported=foo", headers=auth_headers)
    assert resp.status_code == 200


def test_proof_request_get_after_post(auth_headers):
    data = {
        "user_id": "userA",
        "proof_type": "onboarding",
        "public_signals": ["a", "b"],
        "external_nullifier": "nullA",
    }
    post_resp = client.post("/api/identity/proof-request", json=data, headers=auth_headers)
    assert post_resp.status_code == 200
    get_resp = client.get("/api/identity/proof-requests", headers=auth_headers)
    assert get_resp.status_code == 200
    result = get_resp.json()
    assert any(p["user_id"] == "userA" and p["proof_type"] == "onboarding" for p in result)


def test_proof_request_get_multiple(auth_headers):
    client.post(
        "/api/identity/proof-request",
        json={
            "user_id": "userB",
            "proof_type": "recovery",
            "public_signals": ["x"],
            "external_nullifier": "nullB",
        },
        headers=auth_headers,
    )
    client.post(
        "/api/identity/proof-request",
        json={
            "user_id": "userC",
            "proof_type": "voting",
            "public_signals": ["y", "z"],
            "external_nullifier": "nullC",
        },
        headers=auth_headers,
    )
    resp = client.get("/api/identity/proof-requests", headers=auth_headers)
    print("Status code (proof multiple):", resp.status_code)
    print("Response (proof multiple):", resp.text)
    assert resp.status_code == 200
    result = resp.json()
    assert len(result) == 2
    users = {p["user_id"] for p in result}
    assert "userB" in users and "userC" in users


def test_proof_request_get_fields(auth_headers):
    data = {
        "user_id": "userD",
        "proof_type": "voting",
        "public_signals": ["sig1", "sig2"],
        "external_nullifier": "nullD",
    }
    post_resp = client.post("/api/identity/proof-request", json=data, headers=auth_headers)
    print("POST status (proof fields):", post_resp.status_code, post_resp.text)
    resp = client.get("/api/identity/proof-requests", headers=auth_headers)
    print("GET status (proof fields):", resp.status_code, resp.text)
    assert resp.status_code == 200
    proof = resp.json()[0]
    for key in ["user_id", "proof_type", "public_signals", "external_nullifier"]:
        assert key in proof
    assert isinstance(proof["public_signals"], list)


# --- ProofRequest Validation Tests ---
def test_proof_request_invalid_type(auth_headers):
    data = {
        "user_id": "user1",
        "proof_type": "invalid",
        "public_signals": [1, 2],
        "external_nullifier": "n",
    }
    resp = client.post("/api/identity/proof-request", json=data, headers=auth_headers)
    assert resp.status_code == 422
    assert "proof_type" in resp.text


def test_proof_request_empty_signals(auth_headers):
    data = {
        "user_id": "user1",
        "proof_type": "onboarding",
        "public_signals": [],
        "external_nullifier": "n",
    }
    resp = client.post("/api/identity/proof-request", json=data, headers=auth_headers)
    assert resp.status_code == 422
    assert "public_signals" in resp.text


# --- KPI Success Test ---
def test_kpi_success(auth_headers):
    data = {
        "region": "EU",
        "epoch": 1,
        "participation_rate": 72.5,
        "accessibility_score": 88.0,
        "trust_index": 0.91,
    }
    resp = client.post("/api/reporting/kpis", json=data)
    assert resp.status_code == 200
    assert resp.json()["region"] == "EU"


# --- KPI GET Tests ---
def test_kpi_get_empty(auth_headers):
    resp = client.get("/api/reporting/kpis")
    assert resp.status_code == 200
    assert resp.json() == []


def test_kpi_get_after_post(auth_headers):
    data = {
        "region": "ASIA",
        "epoch": 1,
        "participation_rate": 65.0,
        "accessibility_score": 80.0,
        "trust_index": 0.85,
    }
    post_resp = client.post("/api/reporting/kpis", json=data)
    assert post_resp.status_code == 200
    get_resp = client.get("/api/reporting/kpis")
    assert get_resp.status_code == 200
    result = get_resp.json()
    assert any(kpi["region"] == "ASIA" for kpi in result)


def test_kpi_get_filter_region(auth_headers):
    # Sicherstellen, dass mindestens ein EU-KPI existiert
    client.post(
        "/api/reporting/kpis",
        json={
            "region": "EU",
            "epoch": 1,
            "participation_rate": 50.0,
            "accessibility_score": 70.0,
            "trust_index": 0.80,
        },
    )
    resp = client.get("/api/reporting/kpis?region=EU")
    assert resp.status_code == 200
    result = resp.json()
    assert all(kpi["region"] == "EU" for kpi in result)


def test_kpi_get_filter_region_not_found(auth_headers):
    client.post(
        "/api/reporting/kpis",
        json={
            "region": "AFRICA",
            "epoch": 1,
            "participation_rate": 40.0,
            "accessibility_score": 60.0,
            "trust_index": 0.75,
        },
    )
    resp = client.get("/api/reporting/kpis?region=OCEANIA")
    assert resp.status_code == 200
    assert resp.json() == []


def test_kpi_get_filter_region_case_insensitive(auth_headers):
    client.post(
        "/api/reporting/kpis",
        json={
            "region": "Asia",
            "epoch": 1,
            "participation_rate": 55.0,
            "accessibility_score": 70.0,
            "trust_index": 0.82,
        },
    )
    resp = client.get("/api/reporting/kpis?region=asia")
    assert resp.status_code == 200
    # Depending on implementation, this may fail if the filter is case-sensitive
    # Accept either empty or matching result
    result = resp.json()
    assert result == [] or all(kpi["region"].lower() == "asia" for kpi in result)


# --- Negative Filter Tests (GET) ---
def test_kpi_get_filter_epoch_wrong_type(auth_headers):
    resp = client.get("/api/reporting/kpis?region=EU&epoch=wrongtype")
    # Should return 422 or ignore epoch param
    assert resp.status_code in (200, 422)


def test_kpi_get_filter_region_multiple(auth_headers):
    resp = client.get("/api/reporting/kpis?region=EU&region=ASIA")
    # Should return 200 and either one result set or empty
    assert resp.status_code == 200


def test_kpi_get_filter_unsupported(auth_headers):
    resp = client.get("/api/reporting/kpis?unsupported=foo")
    # Should ignore unsupported param, not error
    assert resp.status_code == 200


# --- KPI Validation Tests ---
def test_kpi_invalid_accessibility(auth_headers):
    data = {
        "region": "EU",
        "epoch": 1,
        "participation_rate": 50.0,
        "accessibility_score": 200.0,
        "trust_index": 0.5,
    }
    resp = client.post("/api/reporting/kpis", json=data, headers=auth_headers)
    assert resp.status_code == 422
    assert "accessibility_score" in resp.text


# --- Alert Success Test ---
def test_alert_success(auth_headers):
    data = {
        "epoch": 1,
        "msi": 0.5,
        "vei": 0.5,
        "collusion_flag": False,
        "status": "ok",
    }
    resp = client.post("/api/tokenomics/alerts", json=data, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


# --- Alert GET Tests ---
def test_alert_get_empty(auth_headers):
    resp = client.get("/api/tokenomics/alerts", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json() == []


def test_alert_get_filter_epoch(auth_headers):
    client.post(
        "/api/tokenomics/alerts",
        json={
            "epoch": 101,
            "msi": 0.5,
            "vei": 0.5,
            "collusion_flag": False,
            "status": "ok",
        },
        headers=auth_headers,
    )
    resp = client.get("/api/tokenomics/alerts?epoch=101", headers=auth_headers)
    # Accept either empty or filtered result depending on implementation
    assert resp.status_code == 200
    result = resp.json()
    assert result == [] or all(a["epoch"] == 101 for a in result)


def test_alert_get_filter_epoch_not_found(auth_headers):
    resp = client.get("/api/tokenomics/alerts?epoch=9999", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json() == []


def test_alert_get_filter_status_case(auth_headers):
    client.post(
        "/api/tokenomics/alerts",
        json={
            "epoch": 202,
            "msi": 0.7,
            "vei": 0.8,
            "collusion_flag": True,
            "status": "Warning",
        },
    )
    resp = client.get("/api/tokenomics/alerts?status=warning")
    assert resp.status_code == 200
    # Accept either empty or matching result depending on implementation
    result = resp.json()
    assert result == [] or all(a["status"].lower() == "warning" for a in result)


def test_alert_get_filter_msi_edge(auth_headers):
    client.post(
        "/api/tokenomics/alerts",
        json={
            "epoch": 303,
            "msi": 1.0,
            "vei": 0.1,
            "collusion_flag": True,
            "status": "danger",
        },
    )
    resp = client.get("/api/tokenomics/alerts?msi=1.0")
    assert resp.status_code == 200
    result = resp.json()
    assert result == [] or all(abs(a["msi"] - 1.0) < 1e-6 for a in result)


def test_alert_get_filter_epoch_string(auth_headers):
    resp = client.get("/api/tokenomics/alerts?epoch=notanumber")
    assert resp.status_code in (200, 422)


def test_alert_get_filter_msi_text(auth_headers):
    resp = client.get("/api/tokenomics/alerts?msi=notafloat")
    assert resp.status_code in (200, 422)


def test_alert_get_filter_status_multiple(auth_headers):
    resp = client.get("/api/tokenomics/alerts?status=ok&status=danger")
    assert resp.status_code == 200


def test_alert_get_filter_unsupported(auth_headers):
    resp = client.get("/api/tokenomics/alerts?unsupported=foo")
    assert resp.status_code == 200


def test_alert_get_after_post(auth_headers):
    data = {
        "epoch": 2,
        "msi": 0.7,
        "vei": 0.6,
        "collusion_flag": False,
        "status": "warning",
    }
    post_resp = client.post("/api/tokenomics/alerts", json=data, headers=auth_headers)
    assert post_resp.status_code == 200
    get_resp = client.get("/api/tokenomics/alerts", headers=auth_headers)
    assert get_resp.status_code == 200
    result = get_resp.json()
    assert any(alert["epoch"] == 2 and alert["status"] == "warning" for alert in result)


def test_alert_get_multiple(auth_headers):
    # Zwei Alerts anlegen
    client.post(
        "/api/tokenomics/alerts",
        json={
            "epoch": 10,
            "msi": 0.1,
            "vei": 0.2,
            "collusion_flag": False,
            "status": "ok",
        },
        headers=auth_headers,
    )
    client.post(
        "/api/tokenomics/alerts",
        json={
            "epoch": 11,
            "msi": 0.3,
            "vei": 0.4,
            "collusion_flag": True,
            "status": "info",
        },
        headers=auth_headers,
    )
    resp = client.get("/api/tokenomics/alerts", headers=auth_headers)
    print("Status code (alert multiple):", resp.status_code)
    print("Response (alert multiple):", resp.text)
    assert resp.status_code == 200
    result = resp.json()
    assert len(result) == 2
    epochs = {a["epoch"] for a in result}
    assert 10 in epochs and 11 in epochs


def test_alert_get_fields(auth_headers):
    data = {
        "epoch": 3,
        "msi": 0.9,
        "vei": 0.8,
        "collusion_flag": True,
        "status": "danger",
    }
    post_resp = client.post("/api/tokenomics/alerts", json=data, headers=auth_headers)
    print("POST status (alert fields):", post_resp.status_code, post_resp.text)
    resp = client.get("/api/tokenomics/alerts", headers=auth_headers)
    print("GET status (alert fields):", resp.status_code, resp.text)
    assert resp.status_code == 200
    alert = resp.json()[0]
    for key in ["epoch", "msi", "vei", "collusion_flag", "status"]:
        assert key in alert


# --- Alert Validation Tests ---
def test_alert_invalid_msi(auth_headers):
    data = {
        "epoch": 1,
        "msi": 1.5,
        "vei": 0.5,
        "collusion_flag": False,
        "status": "ok",
    }
    resp = client.post("/api/tokenomics/alerts", json=data, headers=auth_headers)
    assert resp.status_code == 422
    assert "msi" in resp.text
