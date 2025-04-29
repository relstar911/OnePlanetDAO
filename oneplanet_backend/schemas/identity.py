from pydantic import BaseModel
from typing import List, Literal

class ProofRequest(BaseModel):
    user_id: str
    proof_type: Literal["onboarding","recovery","voting"]
    public_signals: List[str]
    external_nullifier: str

class ProofResponse(BaseModel):
    proof: str
    status: str

class AppealRequest(BaseModel):
    user_id: str
    reason: str
    details: str = ""

class AppealResponse(BaseModel):
    status: str
    case_id: str

class LoginRequest(BaseModel):
    user_id: str
    password: str = ""  # Für späteres echtes Login, aktuell Dummy
