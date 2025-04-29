import pytest
from sqlmodel import Session, SQLModel, create_engine, select
from oneplanet_backend.core.privacy import AuditLog, PrivacyClass, audit_log_access
from datetime import datetime


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_audit_log_access_creates_entry(session, monkeypatch):
    # Patch get_session to yield our test session
    from oneplanet_backend.core import privacy

    monkeypatch.setattr(privacy, "get_session", lambda: iter([session]))

    user_id = "user123"
    model = "Vote"
    model_id = "proposal456"
    action = "POST /vote"
    privacy_class = PrivacyClass.MEMBER_ONLY
    reason = "Vote submitted"

    audit_log_access(user_id, model, model_id, action, privacy_class, reason)
    # Query the AuditLog table
    logs = session.exec(select(AuditLog)).all()
    assert len(logs) == 1
    log = logs[0]
    assert log.user_id == user_id
    assert log.model == model
    assert log.model_id == model_id
    assert log.action == action
    assert log.privacy_class == privacy_class
    assert log.reason == reason
    assert isinstance(log.timestamp, datetime)
