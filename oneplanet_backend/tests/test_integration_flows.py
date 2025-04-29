import pytest
from fastapi.testclient import TestClient
from oneplanet_backend.main import app

client = TestClient(app)

# --- Integration/E2E: Onboarding to Voting Flow ---
def test_full_onboarding_to_voting_flow():
    # Step 1: Onboard user with proof request
    proof_data = {
        "user_id": "integrationUser",
        "proof_type": "onboarding",
        "public_signals": ["sigA", "sigB"],
        "external_nullifier": "nullInt"
    }
    proof_resp = client.post("/api/identity/proof-request", json=proof_data)
    assert proof_resp.status_code == 200
    assert proof_resp.json()["status"] == "success"

    # Step 2: Submit KPI for region
    kpi_data = {
        "region": "INTREGION",
        "onRampSuccess": 1,
        "accessibilityScore": 0.9,
        "privacyShieldOptIn": 1,
        "empowermentKPI": 3
    }
    kpi_resp = client.post("/api/reporting/kpis", json=kpi_data)
    assert kpi_resp.status_code == 200
    # Step 3: Create alert for the epoch
    alert_data = {
        "epoch": 99,
        "msi": 0.95,
        "vei": 0.85,
        "collusion": "none",
        "status": "ok",
        "alert": "integration test"
    }
    alert_resp = client.post("/api/tokenomics/alerts", json=alert_data)
    assert alert_resp.status_code == 200
    # Step 4: Cast a vote
    vote_data = {
        "user_id": "integrationUser",
        "proposal_id": "intProp",
        "vote_weights": {"A": 1, "B": 2},
        "proof": "intProof"
    }
    vote_resp = client.post("/api/governance/vote", json=vote_data)
    assert vote_resp.status_code == 200
    assert vote_resp.json()["status"] == "success"
    # Step 5: Query all entities and check linkage
    proof_get = client.get("/api/identity/proof-requests?user_id=integrationUser")
    assert proof_get.status_code == 200
    assert any(p["user_id"] == "integrationUser" for p in proof_get.json())
    vote_get = client.get("/api/governance/votes?user_id=integrationUser")
    assert vote_get.status_code == 200
    assert any(v["user_id"] == "integrationUser" for v in vote_get.json())
    kpi_get = client.get("/api/reporting/kpis?region=INTREGION")
    assert kpi_get.status_code == 200
    assert any(k["region"] == "INTREGION" for k in kpi_get.json())
    alert_get = client.get("/api/tokenomics/alerts?epoch=99")
    assert alert_get.status_code == 200
    assert any(a["epoch"] == 99 for a in alert_get.json())

# --- Integration/E2E: Negative Flow ---
def test_onboarding_vote_missing_proof():
    # Try to vote with a user that has not onboarded
    vote_data = {
        "user_id": "notOnboarded",
        "proposal_id": "failProp",
        "vote_weights": {"X": 1},
        "proof": "failProof"
    }
    vote_resp = client.post("/api/governance/vote", json=vote_data)
    # Should still succeed unless onboarding is enforced, but check for 200 or 422
    assert vote_resp.status_code in (200, 422)

# --- Integration/E2E: Double ProofRequest for Same User ---
def test_double_proof_request_same_user():
    data = {
        "user_id": "doubleUser",
        "proof_type": "onboarding",
        "public_signals": ["d1"],
        "external_nullifier": "dnull"
    }
    resp1 = client.post("/api/identity/proof-request", json=data)
    resp2 = client.post("/api/identity/proof-request", json=data)
    assert resp1.status_code == 200
    # Depending on logic, double onboarding may be allowed or rejected
    assert resp2.status_code in (200, 422)

# --- Integration/E2E: Vote with Invalid ProofType ---
def test_vote_with_invalid_proof_type():
    data = {
        "user_id": "invalidProofType",
        "proof_type": "invalid",
        "public_signals": ["x"],
        "external_nullifier": "nullx"
    }
    resp = client.post("/api/identity/proof-request", json=data)
    assert resp.status_code == 422

# --- Integration/E2E: Alert with Edge MSI/VEI ---
def test_alert_with_edge_msi_vei():
    for msi, vei in [(0.0, 0.0), (1.0, 1.0)]:
        data = {
            "epoch": 777,
            "msi": msi,
            "vei": vei,
            "collusion": "none",
            "status": "ok",
            "alert": f"edge msi={msi} vei={vei}"
        }
        resp = client.post("/api/tokenomics/alerts", json=data)
        assert resp.status_code == 200
        get_resp = client.get(f"/api/tokenomics/alerts?epoch=777&msi={msi}")
        assert get_resp.status_code == 200
        assert any(abs(a["msi"] - msi) < 1e-6 for a in get_resp.json())

# --- Integration/E2E: Parallel User Flows ---
def test_parallel_user_flows():
    # User X
    proof_x = client.post("/api/identity/proof-request", json={
        "user_id": "userX",
        "proof_type": "onboarding",
        "public_signals": ["x1"],
        "external_nullifier": "nx"
    })
    assert proof_x.status_code == 200
    vote_x = client.post("/api/governance/vote", json={
        "user_id": "userX",
        "proposal_id": "propX",
        "vote_weights": {"A": 1},
        "proof": "proofX"
    })
    assert vote_x.status_code == 200
    # User Y
    proof_y = client.post("/api/identity/proof-request", json={
        "user_id": "userY",
        "proof_type": "onboarding",
        "public_signals": ["y1"],
        "external_nullifier": "ny"
    })
    assert proof_y.status_code == 200
    vote_y = client.post("/api/governance/vote", json={
        "user_id": "userY",
        "proposal_id": "propY",
        "vote_weights": {"B": 2},
        "proof": "proofY"
    })
    assert vote_y.status_code == 200
    # Check both users are present
    votes = client.get("/api/governance/votes")
    assert any(v["user_id"] == "userX" for v in votes.json())
    assert any(v["user_id"] == "userY" for v in votes.json())

# --- Integration/E2E: Vote on Nonexistent ProposalID ---
def test_vote_on_nonexistent_proposal():
    data = {
        "user_id": "userZ",
        "proposal_id": "doesNotExist",
        "vote_weights": {"A": 1},
        "proof": "proofZ"
    }
    resp = client.post("/api/governance/vote", json=data)
    # Should succeed unless proposal existence is enforced
    assert resp.status_code in (200, 422)
