from pydantic import BaseModel


class ProposalCreate(BaseModel):
    proposal_id: str
    title: str
    description: str = ""


class ProposalResponse(BaseModel):
    id: int
    proposal_id: str
    title: str
    description: str


class VoteRequest(BaseModel):
    user_id: str
    proposal_id: str
    vote_weights: dict[str, int]
    proof: str


class VoteResponse(BaseModel):
    status: str
    tx_hash: str
