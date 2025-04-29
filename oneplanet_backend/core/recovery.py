# recovery.py – Datenmodelle für Social Recovery & Guardians
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, JSON


class GuardianAssignment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str  # Nutzer, der Guardians zuordnet
    guardian_id: str  # Vertrauensperson
    status: str = "active"  # active, pending, revoked
    added_at: datetime = Field(default_factory=datetime.utcnow)


class RecoveryRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str  # Account, der wiederhergestellt werden soll
    initiator_id: str  # Wer startet den Prozess (user_id oder guardian_id)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"  # pending, approved, denied, completed
    approvals: List[str] = Field(
        sa_column=Column(JSON), default_factory=list
    )  # guardian_ids, die zugestimmt haben
    threshold: int = 2  # Wie viele Guardians müssen zustimmen?
