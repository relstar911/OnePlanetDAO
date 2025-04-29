from pydantic import BaseModel
from typing import Dict


class VoteRequest(BaseModel):
    user_id: str
    proposal_id: str
    vote_weights: Dict[str, int]
    proof: str


class VoteResponse(BaseModel):
    status: str
    tx_hash: str
