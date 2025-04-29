from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    region: str

class Proposal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    proposal_id: str
    title: str
    description: str

class Vote(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    proposal_id: str
    vote_weights: str  # JSON-encoded dict
    proof: str

class ProofRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    proof_type: str
    public_signals: str  # JSON-encoded list
    external_nullifier: str

class Alert(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    epoch: int
    msi: float
    vei: float
    collusion: str
    status: str
    alert: str

class KPI(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    region: str
    onRampSuccess: int
    accessibilityScore: float
    privacyShieldOptIn: int
    empowermentKPI: int
