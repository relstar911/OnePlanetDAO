from fastapi.testclient import TestClient
from oneplanet_backend.main import app

client = TestClient(app)


def test_kpis_missing_required_fields():
    resp = client.post("/api/reporting/kpis", json={})
    assert resp.status_code in (400, 422)
    data = resp.json()
    assert "detail" in data
    if isinstance(data["detail"], list):
        assert any("msg" in err for err in data["detail"])
    else:
        assert (
            "field required" in data["detail"]
            or "Unprocessable Entity" in data["detail"]
            or "Missing required KPI fields" in data["detail"]
        )


def test_proof_request_missing_fields():
    resp = client.post("/api/identity/proof-request", json={})
    assert resp.status_code in (400, 401, 403, 422)
    data = resp.json()
    assert "detail" in data
    # FastAPI returns validation errors as a list for 422
    if isinstance(data["detail"], list):
        assert any("msg" in err for err in data["detail"])
    else:
        assert (
            "required" in data["detail"]
            or "missing" in data["detail"]
            or "Not authenticated" in data["detail"]
        )


def test_vote_missing_auth():
    payload = {
        "user_id": "user123",
        "proposal_id": "prop1",
        "vote_weights": {"optionA": 2},
        "proof": "proofdata",
    }
    resp = client.post("/api/governance/vote", json=payload)
    assert resp.status_code in (401, 403)
    data = resp.json()
    assert "detail" in data
    assert "Not authenticated" in data["detail"] or "credentials" in data["detail"]


def test_vote_invalid_payload():
    resp = client.post("/api/governance/vote", json={})
    assert resp.status_code in (400, 401, 403, 422)
    data = resp.json()
    assert "detail" in data
    if isinstance(data["detail"], list):
        assert any("msg" in err for err in data["detail"])
    else:
        assert (
            "required" in data["detail"]
            or "missing" in data["detail"]
            or "Not authenticated" in data["detail"]
        )
