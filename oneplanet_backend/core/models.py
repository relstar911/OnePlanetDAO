from sqlmodel import Field, SQLModel

from .privacy import PrivacyClass, privacy_class


@privacy_class(PrivacyClass.REDACTED)
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str
    region: str


@privacy_class(PrivacyClass.PUBLIC)
class Proposal(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    proposal_id: str
    title: str
    description: str


@privacy_class(PrivacyClass.MEMBER_ONLY)
class Vote(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str
    proposal_id: str
    vote_weights: str  # JSON-encoded dict
    proof: str


@privacy_class(PrivacyClass.MEMBER_ONLY)
class ProofRequest(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str
    proof_type: str
    public_signals: str  # JSON-encoded list
    external_nullifier: str


@privacy_class(PrivacyClass.PUBLIC)
class Alert(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    epoch: int
    msi: float
    vei: float
    collusion_flag: bool = False
    status: str


@privacy_class(PrivacyClass.PUBLIC)
class KPI(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    region: str
    epoch: int = 1
    participation_rate: float = 0.0
    accessibility_score: float = 0.0
    trust_index: float = 0.0
