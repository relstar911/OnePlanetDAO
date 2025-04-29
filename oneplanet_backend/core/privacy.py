"""
Privacy and Audit Logging Module
- PrivacyClass Enum: Defines privacy levels for data models
- AuditLog SQLModel: Stores access events for sensitive data
- privacy_class decorator: Attach privacy class to models
- audit_log_access: Function to log access events
"""

from enum import Enum
from sqlmodel import SQLModel, Field, Session
from datetime import datetime
from .db import get_session


class PrivacyClass(str, Enum):
    PUBLIC = "public"
    MEMBER_ONLY = "member_only"
    REDACTED = "redacted"


class AuditLog(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    model: str
    model_id: str
    action: str
    privacy_class: PrivacyClass
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    reason: str = ""


def privacy_class(level: PrivacyClass):
    """Decorator to attach privacy class metadata to SQLModel classes."""

    def decorator(cls):
        cls.__privacy_class__ = level
        return cls

    return decorator


def audit_log_access(
    user_id: str,
    model: str,
    model_id: str,
    action: str,
    privacy_class: PrivacyClass,
    reason: str = "",
    session: Session = None,
):
    """Logs access to sensitive data in the AuditLog table. Optional: use existing session."""
    log = AuditLog(
        user_id=user_id,
        model=model,
        model_id=model_id,
        action=action,
        privacy_class=privacy_class,
        reason=reason,
    )
    if session is not None:
        session.add(log)
        session.commit()
    else:
        with next(get_session()) as s:
            s.add(log)
            s.commit()
