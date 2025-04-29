# test_recovery_api.py – Tests für Social Recovery & Guardians API
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from oneplanet_backend.main import app
from oneplanet_backend.core.db import engine

from oneplanet_backend.core.privacy import AuditLog, PrivacyClass
from sqlalchemy import text, select

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    # Vor jedem Test: Recovery-Tabellen leeren
    with Session(engine) as session:
        session.exec(text("DELETE FROM guardianassignment"))
        session.exec(text("DELETE FROM recoveryrequest"))
        session.commit()


def test_add_and_remove_guardian():
    # Guardian hinzufügen
    resp = client.post("/api/identity/guardians", params={"user_id": "alice", "guardian_id": "bob"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["user_id"] == "alice"
    assert data["guardian_id"] == "bob"
    # Guardian entfernen
    resp = client.delete(
        "/api/identity/guardians", params={"user_id": "alice", "guardian_id": "bob"}
    )
    assert resp.status_code == 200
    assert resp.json()["msg"] == "Guardian revoked."


def test_start_and_approve_recovery():
    # Recovery-Prozess starten
    resp = client.post(
        "/api/identity/recovery-request",
        params={"user_id": "alice", "initiator_id": "alice", "threshold": 2},
    )
    assert resp.status_code == 200
    req = resp.json()
    assert req["user_id"] == "alice"
    assert req["status"] == "pending"
    # Approve durch Guardian 1
    resp = client.post(
        "/api/identity/recovery-approve", params={"request_id": req["id"], "guardian_id": "bob"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == req["id"]
    assert "bob" in data["approvals"]
    # Approve durch Guardian 2 (Threshold erreicht)
    resp = client.post(
        "/api/identity/recovery-approve", params={"request_id": req["id"], "guardian_id": "carol"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "approved"
    assert set(data["approvals"]) == {"bob", "carol"}


def test_get_recovery_status():
    # Recovery-Prozess starten
    resp = client.post(
        "/api/identity/recovery-request", params={"user_id": "alice", "initiator_id": "alice"}
    )
    assert resp.status_code == 200
    req = resp.json()
    # Status abfragen
    resp = client.get(f"/api/identity/recovery-status?request_id={req['id']}")
    assert resp.status_code == 200
    status_data = resp.json()
    assert status_data["id"] == req["id"]


def test_guardian_double_add():
    resp = client.post("/api/identity/guardians", params={"user_id": "alice", "guardian_id": "bob"})
    assert resp.status_code == 200
    # Nochmal hinzufügen (soll 400 liefern)
    resp = client.post("/api/identity/guardians", params={"user_id": "alice", "guardian_id": "bob"})
    assert resp.status_code == 400
    assert "already assigned" in resp.json()["detail"].lower()


def test_double_approve():
    resp = client.post(
        "/api/identity/recovery-request",
        params={"user_id": "alice", "initiator_id": "alice", "threshold": 2},
    )
    assert resp.status_code == 200
    req = resp.json()
    # Approve durch bob
    resp = client.post(
        "/api/identity/recovery-approve", params={"request_id": req["id"], "guardian_id": "bob"}
    )
    assert resp.status_code == 200
    # Nochmal approve durch bob (soll 400 liefern)
    resp = client.post(
        "/api/identity/recovery-approve", params={"request_id": req["id"], "guardian_id": "bob"}
    )
    assert resp.status_code == 400
    assert "already approved" in resp.json()["detail"].lower()


def test_approve_after_threshold():
    resp = client.post(
        "/api/identity/recovery-request",
        params={"user_id": "alice", "initiator_id": "alice", "threshold": 1},
    )
    assert resp.status_code == 200
    req = resp.json()
    # Approve durch bob (Threshold erreicht)
    resp = client.post(
        "/api/identity/recovery-approve", params={"request_id": req["id"], "guardian_id": "bob"}
    )
    assert resp.status_code == 200
    # Approve durch carol (soll trotzdem gehen, aber Status bleibt approved)
    resp = client.post(
        "/api/identity/recovery-approve", params={"request_id": req["id"], "guardian_id": "carol"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "approved"
    assert set(data["approvals"]) == {"bob", "carol"}


def test_approve_invalid_request():
    resp = client.post(
        "/api/identity/recovery-approve", params={"request_id": 9999, "guardian_id": "bob"}
    )
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()


def test_status_invalid_request():
    resp = client.get("/api/identity/recovery-status?request_id=9999")
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()

    # Recovery-Prozess starten
    resp = client.post(
        "/api/identity/recovery-request", params={"user_id": "alice", "initiator_id": "alice"}
    )
    assert resp.status_code == 200
    req = resp.json()
    # Status abfragen
    resp = client.get(f"/api/identity/recovery-status?request_id={req['id']}")
    assert resp.status_code == 200
    status_data = resp.json()
    assert status_data["id"] == req["id"]
    assert status_data["status"] == "pending"


def test_deny_recovery():
    # Recovery-Prozess starten
    resp = client.post(
        "/api/identity/recovery-request", params={"user_id": "alice", "initiator_id": "alice"}
    )
    assert resp.status_code == 200
    req = resp.json()
    # Deny durch bob
    resp = client.post(
        "/api/identity/recovery-deny",
        params={"request_id": req["id"], "denier_id": "bob", "reason": "nope"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "denied"
    # AuditLog prüfen
    with Session(engine) as session:
        logs = list(
            session.exec(
                select(AuditLog).where(
                    AuditLog.model == "RecoveryRequest", AuditLog.action == "DENY_RECOVERY"
                )
            ).scalars()
        )
        assert any(
            log_entry.user_id == "bob" and log_entry.privacy_class == PrivacyClass.MEMBER_ONLY
            for log_entry in logs
        )
    # Doppelte Denial
    resp = client.post(
        "/api/identity/recovery-deny", params={"request_id": req["id"], "denier_id": "carol"}
    )
    assert resp.status_code == 404
    # Ungültige ID
    resp = client.post(
        "/api/identity/recovery-deny", params={"request_id": 9999, "denier_id": "bob"}
    )
    assert resp.status_code == 404


def test_auditlog_recovery_flows():
    """Testet, ob bei allen Recovery/Guardian-Aktionen AuditLog-Einträge erzeugt werden."""
    with Session(engine) as session:
        session.exec(text("DELETE FROM auditlog"))
        session.commit()

    # Guardian hinzufügen
    resp = client.post("/api/identity/guardians", params={"user_id": "alice", "guardian_id": "bob"})
    assert resp.status_code == 200
    with Session(engine) as session:
        logs = list(
            session.exec(
                select(AuditLog).where(
                    AuditLog.model == "GuardianAssignment", AuditLog.action == "ADD_GUARDIAN"
                )
            ).scalars()
        )
        assert any(
            log_entry.user_id == "alice" and log_entry.privacy_class == PrivacyClass.MEMBER_ONLY
            for log_entry in logs
        )

    # Guardian entfernen
    resp = client.delete(
        "/api/identity/guardians", params={"user_id": "alice", "guardian_id": "bob"}
    )
    assert resp.status_code == 200
    with Session(engine) as session:
        logs = list(
            session.exec(
                select(AuditLog).where(
                    AuditLog.model == "GuardianAssignment", AuditLog.action == "REMOVE_GUARDIAN"
                )
            ).scalars()
        )
        assert any(
            log_entry.user_id == "alice" and log_entry.privacy_class == PrivacyClass.MEMBER_ONLY
            for log_entry in logs
        )

    # Recovery-Prozess starten
    resp = client.post(
        "/api/identity/recovery-request",
        params={"user_id": "alice", "initiator_id": "alice", "threshold": 2},
    )
    assert resp.status_code == 200
    req = resp.json()
    with Session(engine) as session:
        logs = list(
            session.exec(
                select(AuditLog).where(
                    AuditLog.model == "RecoveryRequest", AuditLog.action == "START_RECOVERY"
                )
            ).scalars()
        )
        assert any(
            log_entry.user_id == "alice" and log_entry.privacy_class == PrivacyClass.MEMBER_ONLY
            for log_entry in logs
        )

    # Recovery approval durch bob
    resp = client.post(
        "/api/identity/recovery-approve", params={"request_id": req["id"], "guardian_id": "bob"}
    )
    assert resp.status_code == 200
    with Session(engine) as session:
        logs = list(
            session.exec(
                select(AuditLog).where(
                    AuditLog.model == "RecoveryRequest", AuditLog.action == "APPROVE_RECOVERY"
                )
            ).scalars()
        )
        assert any(
            log_entry.user_id == "bob" and log_entry.privacy_class == PrivacyClass.MEMBER_ONLY
            for log_entry in logs
        )

    resp = client.get("/api/identity/recovery-status?request_id=9999")
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()

    # Recovery-Prozess starten
    resp = client.post(
        "/api/identity/recovery-request", params={"user_id": "alice", "initiator_id": "alice"}
    )
    assert resp.status_code == 200
    req = resp.json()
    # Status abfragen
    resp = client.get(f"/api/identity/recovery-status?request_id={req['id']}")
    assert resp.status_code == 200
    status_data = resp.json()
    assert status_data["id"] == req["id"]
    assert status_data["status"] == "pending"
