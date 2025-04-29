import os
import pytest
import time
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session, select

from oneplanet_backend.core.privacy import AuditLog

DB_PATH = "./test_api_auditlog_minimal.db"
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
engine = create_engine(f"sqlite:///{DB_PATH}")
SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.post("/auditlog-test")
def create_auditlog_entry(session: Session = Depends(get_session)):
    log = AuditLog(
        user_id="api-user",
        model="APIModel",
        model_id="api-id",
        action="API-POST",
        privacy_class="PUBLIC",
        reason="api-test",
    )
    session.add(log)
    session.commit()
    return {"success": True}


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_auditlog_insert_and_select():
    # Insert direkt
    with Session(engine) as session:
        log = AuditLog(
            user_id="u1",
            model="ProofRequest",
            model_id="mid1",
            action="POST",
            privacy_class="PUBLIC",
            reason="test",
        )
        session.add(log)
        session.commit()
    # Select direkt
    with Session(engine) as session:
        logs = session.exec(select(AuditLog)).all()
        assert any(log.model == "ProofRequest" for log in logs)


def test_auditlog_via_api(client):
    # Schreibe über API
    resp = client.post("/auditlog-test")
    assert resp.status_code == 200
    # Überprüfe DB
    with Session(engine) as session:
        logs = session.exec(select(AuditLog)).all()
        assert any(log.model == "APIModel" for log in logs)


@pytest.fixture(scope="session", autouse=True)
def cleanup_db():
    yield
    for _ in range(5):
        try:
            if os.path.exists(DB_PATH):
                os.remove(DB_PATH)
            break
        except PermissionError:
            time.sleep(0.2)
