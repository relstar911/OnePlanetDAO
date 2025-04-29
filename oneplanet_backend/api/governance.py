from fastapi import APIRouter, Depends
from ..schemas.governance import VoteRequest, VoteResponse
from ..core.db import get_session
from ..core.models import Vote
from sqlmodel import Session, select
import json
from typing import List

router = APIRouter()

@router.post("/vote", response_model=VoteResponse)
def submit_vote(vote: VoteRequest, session: Session = Depends(get_session)):
    """Submit a quadratic vote (see System Blueprint/API Spec)."""
    db_vote = Vote(
        user_id=vote.user_id,
        proposal_id=vote.proposal_id,
        vote_weights=json.dumps(vote.vote_weights),
        proof=vote.proof
    )
    session.add(db_vote)
    session.commit()
    session.refresh(db_vote)
    return VoteResponse(status="success", tx_hash=str(db_vote.id))

@router.get("/votes", response_model=List[VoteRequest])
def list_votes(session: Session = Depends(get_session)):
    votes = session.exec(select(Vote)).all()
    return [
        VoteRequest(
            user_id=v.user_id,
            proposal_id=v.proposal_id,
            vote_weights=json.loads(v.vote_weights),
            proof=v.proof
        ) for v in votes
    ]
