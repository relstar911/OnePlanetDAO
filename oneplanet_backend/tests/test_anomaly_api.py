# test_anomaly_api.py – Testet den Admin-API-Endpunkt für Anomalien
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from oneplanet_backend.main import app
from oneplanet_backend.core.anomaly import AnomalyLog
from oneplanet_backend.core.db import engine
from sqlalchemy import text

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    # Vor jedem Test: DB leeren
    with Session(engine) as session:
        session.exec(text("DELETE FROM anomalylog"))
        session.commit()


def test_anomaly_api_empty():
    resp = client.get("/api/anomaly/anomalies")
    assert resp.status_code == 200
    assert resp.json() == []


def test_anomaly_api_with_data():
    # Füge eine Anomalie hinzu
    with Session(engine) as session:
        anomaly = AnomalyLog(
            type="voting", description="Test Voting Anomaly", user_id="user1", severity="high"
        )
        session.add(anomaly)
        session.commit()
    resp = client.get("/api/anomaly/anomalies")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["type"] == "voting"
    assert data[0]["description"] == "Test Voting Anomaly"
    assert data[0]["user_id"] == "user1"
    assert data[0]["severity"] == "high"
    assert data[0]["resolved"] is False


def test_anomaly_api_filter():
    # Zwei Anomalien, eine resolved
    with Session(engine) as session:
        anomaly1 = AnomalyLog(type="voting", description="A1", user_id="u1", severity="low")
        anomaly2 = AnomalyLog(
            type="login", description="A2", user_id="u2", severity="medium", resolved=True
        )
        session.add(anomaly1)
        session.add(anomaly2)
        session.commit()
    # Filter resolved=false
    resp = client.get("/api/anomaly/anomalies?resolved=false")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["type"] == "voting"
    # Filter type=login
    resp = client.get("/api/anomaly/anomalies?type=login")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["type"] == "login"
    # Filter user_id=u1
    resp = client.get("/api/anomaly/anomalies?user_id=u1")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["user_id"] == "u1"
