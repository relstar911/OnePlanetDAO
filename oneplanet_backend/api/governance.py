from fastapi import APIRouter, Depends
from ..schemas.governance import VoteRequest, VoteResponse
from ..core.db import get_session
from ..core.models import Vote
from sqlmodel import Session, select
import json
from typing import List

router = APIRouter()

from fastapi import HTTPException, status

@router.post("/vote", response_model=VoteResponse)
def submit_vote(vote: VoteRequest, session: Session = Depends(get_session)):
    """
    Submit a quadratic vote (see System Blueprint/API Spec).
    Validierung:
    - Pflichtfelder: user_id, proposal_id, vote_weights, proof
    - Wertebereiche: vote_weights >= 0
    - proof darf nicht leer sein
    """
    # Pflichtfeld-Validierung
    if not vote.user_id or not vote.proposal_id or not vote.vote_weights or not vote.proof:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Alle Felder (user_id, proposal_id, vote_weights, proof) müssen gesetzt sein.")
    # Wertebereich-Validierung
    if not isinstance(vote.vote_weights, dict) or any((not isinstance(v, (int, float)) or v < 0) for v in vote.vote_weights.values()):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Alle vote_weights müssen >= 0 sein und als Dict übergeben werden.")
    # Proof-Format-Validierung (hier: nicht leer, später ZK-Check)
    if not isinstance(vote.proof, str) or not vote.proof.strip():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Proof darf nicht leer sein und muss ein String sein.")

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
