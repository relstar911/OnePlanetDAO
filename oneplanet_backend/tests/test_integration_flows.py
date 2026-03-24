import random
import string

from fastapi.testclient import TestClient

from oneplanet_backend.core.limiter import limiter
from oneplanet_backend.main import app

limiter.enabled = False

client = TestClient(app)


def get_auth_headers(user_id):
    # Register user first, then login
    client.post(
        "/api/identity/register",
        json={"user_id": user_id, "password": "testpass1234"},
    )
    resp = client.post(
        "/api/identity/login",
        json={"user_id": user_id, "password": "testpass1234"},
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# --- Integration/E2E: Onboarding to Voting Flow ---
def test_full_onboarding_to_voting_flow():
    userA = "integrationUserA_" + "".join(
        random.choices(string.ascii_lowercase + string.digits, k=8)
    )
    auth_headers = get_auth_headers(userA)

    # Step 1: Onboard user with proof request
    proof_data = {
        "user_id": userA,
        "proof_type": "onboarding",
        "public_signals": ["sigA", "sigB"],
        "external_nullifier": "nullInt",
    }
    proof_resp = client.post("/api/identity/proof-request", json=proof_data, headers=auth_headers)
    assert proof_resp.status_code == 200
    assert proof_resp.json()["status"] == "success"

    # Step 2: Submit KPI for region
    kpi_data = {
        "region": "INTREGION",
        "epoch": 1,
        "participation_rate": 70.0,
        "accessibility_score": 90.0,
        "trust_index": 0.88,
    }
    kpi_resp = client.post("/api/reporting/kpis", json=kpi_data, headers=auth_headers)
    assert kpi_resp.status_code == 200
    # Step 3: Create alert for the epoch
    alert_data = {
        "epoch": 99,
        "msi": 0.95,
        "vei": 0.85,
        "collusion_flag": False,
        "status": "ok",
    }
    alert_resp = client.post("/api/tokenomics/alerts", json=alert_data, headers=auth_headers)
    assert alert_resp.status_code == 200
    # Step 4: Cast a vote
    vote_data = {
        "user_id": userA,
        "proposal_id": "intProp",
        "vote_weights": {"A": 1, "B": 2},
        "proof": "intProof",
    }
    vote_resp = client.post("/api/governance/vote", json=vote_data, headers=auth_headers)
    assert vote_resp.status_code == 200
    assert vote_resp.json()["status"] == "success"
    # Step 5: Query all entities and check linkage
    proof_get = client.get(f"/api/identity/proof-requests?user_id={userA}")
    assert proof_get.status_code == 200
    assert any(p["user_id"] == userA for p in proof_get.json())
    vote_get = client.get(f"/api/governance/votes?user_id={userA}")
    assert vote_get.status_code == 200
    assert any(v["user_id"] == userA for v in vote_get.json())
    kpi_get = client.get("/api/reporting/kpis?region=INTREGION")
    assert kpi_get.status_code == 200
    assert any(k["region"] == "INTREGION" for k in kpi_get.json())
    alert_get = client.get("/api/tokenomics/alerts?epoch=99")
    assert alert_get.status_code == 200
    assert any(a["epoch"] == 99 for a in alert_get.json())


# --- Integration/E2E: Negative Flow ---
def test_onboarding_vote_missing_proof():
    user = "integrationUser_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    auth_headers = get_auth_headers(user)
    # Try to vote with a user that has not onboarded
    vote_data = {
        "user_id": "notOnboarded",
        "proposal_id": "failProp",
        "vote_weights": {"X": 1},
        "proof": "failProof",
    }
    vote_resp = client.post("/api/governance/vote", json=vote_data, headers=auth_headers)
    # Should still succeed unless onboarding is enforced, but check for 200 or 422
    assert vote_resp.status_code in (200, 422)


# --- Integration/E2E: Double ProofRequest for Same User ---
def test_double_proof_request_same_user():
    user = "doubleUser_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    auth_headers = get_auth_headers(user)
    data = {
        "user_id": user,
        "proof_type": "onboarding",
        "public_signals": ["sig"],
        "external_nullifier": "nullDbl",
    }
    resp1 = client.post("/api/identity/proof-request", json=data, headers=auth_headers)
    assert resp1.status_code == 200
    resp2 = client.post("/api/identity/proof-request", json=data, headers=auth_headers)
    assert resp2.status_code == 200 or resp2.status_code == 409
    # Depending on logic, double onboarding may be allowed or rejected
    assert resp2.status_code in (200, 422)


# --- Integration/E2E: Vote with Invalid ProofType ---
def test_vote_with_invalid_proof_type():
    user = "invalidProofType_" + "".join(
        random.choices(string.ascii_lowercase + string.digits, k=8)
    )
    auth_headers = get_auth_headers(user)
    data = {
        "user_id": user,
        "proof_type": "invalid",
        "public_signals": ["sig"],
        "external_nullifier": "nullInv",
    }
    resp = client.post("/api/identity/proof-request", json=data, headers=auth_headers)
    assert resp.status_code == 422


# --- Integration/E2E: Alert with Edge MSI/VEI ---
def test_alert_with_edge_msi_vei():
    user = "integrationUser_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    auth_headers = get_auth_headers(user)
    for msi, vei in [(0.0, 0.0), (1.0, 1.0)]:
        data = {
            "epoch": 777,
            "msi": msi,
            "vei": vei,
            "collusion_flag": False,
            "status": "ok",
        }
        resp = client.post("/api/tokenomics/alerts", json=data, headers=auth_headers)
        assert resp.status_code == 200
        get_resp = client.get(f"/api/tokenomics/alerts?epoch=777&msi={msi}", headers=auth_headers)
        assert get_resp.status_code == 200
        assert any(abs(a["msi"] - msi) < 1e-6 for a in get_resp.json())


# --- Integration/E2E: Parallel User Flows ---
def test_parallel_user_flows():
    userA = "integrationUserA_" + "".join(
        random.choices(string.ascii_lowercase + string.digits, k=8)
    )
    userB = "integrationUserB_" + "".join(
        random.choices(string.ascii_lowercase + string.digits, k=8)
    )
    headersA = get_auth_headers(userA)
    headersB = get_auth_headers(userB)
    # User X
    proof_x = client.post(
        "/api/identity/proof-request",
        json={
            "user_id": userA,
            "proof_type": "onboarding",
            "public_signals": ["x1"],
            "external_nullifier": "nx",
        },
        headers=headersA,
    )
    assert proof_x.status_code == 200
    vote_x = client.post(
        "/api/governance/vote",
        json={
            "user_id": userA,
            "proposal_id": "propX",
            "vote_weights": {"A": 1},
            "proof": "proofX",
        },
        headers=headersA,
    )
    assert vote_x.status_code == 200
    # User Y
    proof_y = client.post(
        "/api/identity/proof-request",
        json={
            "user_id": userB,
            "proof_type": "onboarding",
            "public_signals": ["y1"],
            "external_nullifier": "ny",
        },
        headers=headersB,
    )
    assert proof_y.status_code == 200
    vote_y = client.post(
        "/api/governance/vote",
        json={
            "user_id": userB,
            "proposal_id": "propY",
            "vote_weights": {"B": 2},
            "proof": "proofY",
        },
        headers=headersB,
    )
    assert vote_y.status_code == 200
    # Check both users are present
    votes = client.get("/api/governance/votes", headers=headersA)
    assert any(v["user_id"] == userA for v in votes.json())
    assert any(v["user_id"] == userB for v in votes.json())


# --- Integration/E2E: Vote on Nonexistent ProposalID ---
def test_vote_on_nonexistent_proposal():
    user = "userZ_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    auth_headers = get_auth_headers(user)
    data = {
        "user_id": user,
        "proposal_id": "doesNotExist",
        "vote_weights": {"A": 1},
        "proof": "proofZ",
    }
    resp = client.post("/api/governance/vote", json=data, headers=auth_headers)
    assert resp.status_code in (200, 422)


# --- Integration/E2E: Full Register → Proposal → Vote → Verify Flow ---
def test_full_register_proposal_vote_verify():
    """Complete E2E: register, login, create proposal, vote, verify all data."""
    uid = "e2e_user_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    pwd = "securepass42"

    # 1. Register
    reg = client.post(
        "/api/identity/register",
        json={"user_id": uid, "password": pwd, "region": "TestRegion"},
    )
    assert reg.status_code == 200
    assert "access_token" in reg.json()
    assert reg.json()["user_id"] == uid

    # 2. Login with same credentials
    login = client.post("/api/identity/login", json={"user_id": uid, "password": pwd})
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Create a proposal
    prop_id = "e2e-prop-" + "".join(random.choices(string.ascii_lowercase, k=6))
    prop = client.post(
        "/api/governance/proposals",
        json={"proposal_id": prop_id, "title": "E2E Test Proposal", "description": "Testing"},
        headers=headers,
    )
    assert prop.status_code == 200
    assert prop.json()["proposal_id"] == prop_id

    # 4. Verify proposal appears in list
    props = client.get("/api/governance/proposals")
    assert props.status_code == 200
    assert any(p["proposal_id"] == prop_id for p in props.json())

    # 5. Submit proof request
    proof = client.post(
        "/api/identity/proof-request",
        json={
            "user_id": uid,
            "proof_type": "voting",
            "public_signals": ["e2e-signal"],
            "external_nullifier": "e2e-null",
        },
        headers=headers,
    )
    assert proof.status_code == 200

    # 6. Vote on the proposal
    vote = client.post(
        "/api/governance/vote",
        json={
            "user_id": uid,
            "proposal_id": prop_id,
            "vote_weights": {"option_a": 3, "option_b": 1},
            "proof": "e2e-zk-proof",
        },
        headers=headers,
    )
    assert vote.status_code == 200
    assert vote.json()["status"] == "success"

    # 7. Verify vote appears
    votes = client.get("/api/governance/votes")
    assert votes.status_code == 200
    my_votes = [v for v in votes.json() if v["user_id"] == uid]
    assert len(my_votes) == 1
    assert my_votes[0]["proposal_id"] == prop_id
    assert my_votes[0]["vote_weights"]["option_a"] == 3

    # 8. Verify proof request appears
    proofs = client.get("/api/identity/proof-requests")
    assert proofs.status_code == 200
    my_proofs = [p for p in proofs.json() if p["user_id"] == uid]
    assert len(my_proofs) == 1
    assert my_proofs[0]["proof_type"] == "voting"

    # 9. Duplicate registration should fail
    dup = client.post(
        "/api/identity/register",
        json={"user_id": uid, "password": "otherpass1234"},
    )
    assert dup.status_code == 409

    # 10. Wrong password login should fail
    bad_login = client.post("/api/identity/login", json={"user_id": uid, "password": "wrong"})
    assert bad_login.status_code == 401


# --- Integration/E2E: Seed endpoint creates full demo data ---
def test_seed_creates_all_entities():
    """Verify seed endpoint creates users, proposals, votes, KPIs, alerts, anomalies."""
    resp = client.post("/api/dev/seed")
    assert resp.status_code == 200
    body = resp.json()
    if body.get("seeded"):
        assert body["counts"]["users"] == 7
        assert body["counts"]["proposals"] == 3
        assert body["counts"]["votes"] == 7
        assert body["counts"]["kpis"] == 5
        assert body["counts"]["alerts"] == 3
        assert body["counts"]["anomalies"] == 3

        # Verify seeded users can login
        login = client.post(
            "/api/identity/login",
            json={"user_id": "alice", "password": "alice1234"},
        )
        assert login.status_code == 200
        assert "access_token" in login.json()

        # Verify proposals exist
        props = client.get("/api/governance/proposals")
        assert len(props.json()) >= 3
