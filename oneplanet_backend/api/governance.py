import json

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session, select

from ..core.auth import require_auth
from ..core.db import get_session
from ..core.limiter import limiter
from ..core.models import PrivacyClass, Vote
from ..core.privacy import audit_log_access
from ..schemas.governance import VoteRequest, VoteResponse
from ..services.quadratic_voting import validate_weights

router = APIRouter()


@router.post("/vote", response_model=VoteResponse)
@limiter.limit("10/minute")
def submit_vote(
    vote: VoteRequest,
    request: Request,
    session: Session = Depends(get_session),  # noqa: B008
    user=Depends(require_auth),  # noqa: B008
):
    """
    Submit a quadratic vote (see System Blueprint/API Spec).
    Validierung:
    - Pflichtfelder: user_id, proposal_id, vote_weights, proof
    - Wertebereiche: vote_weights >= 0
    - proof darf nicht leer sein
    """
    # Audit log: access to sensitive vote submission
    audit_log_access(
        user_id=vote.user_id,
        model="Vote",
        model_id=vote.proposal_id,
        action="POST /vote",
        privacy_class=PrivacyClass.MEMBER_ONLY,
        reason="Vote submitted",
        session=session,
    )
    # Pflichtfeld-Validierung
    if not vote.user_id or not vote.proposal_id or not vote.vote_weights or not vote.proof:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Alle Felder (user_id, proposal_id, vote_weights, proof) müssen gesetzt sein.",
        )
    # Wertebereich-Validierung via QV service
    weight_errors = validate_weights(vote.vote_weights)
    if weight_errors:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=weight_errors[0],
        )
    # Proof-Format-Validierung (hier: nicht leer, später ZK-Check)
    if not isinstance(vote.proof, str) or not vote.proof.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Proof darf nicht leer sein und muss ein String sein.",
        )

    db_vote = Vote(
        user_id=vote.user_id,
        proposal_id=vote.proposal_id,
        vote_weights=json.dumps(vote.vote_weights),
        proof=vote.proof,
    )
    session.add(db_vote)
    session.commit()
    session.refresh(db_vote)
    return VoteResponse(status="success", tx_hash=str(db_vote.id))


@router.get("/votes", response_model=list[VoteRequest])
def list_votes(session: Session = Depends(get_session)):  # noqa: B008
    votes = session.exec(select(Vote)).all()
    return [
        VoteRequest(
            user_id=v.user_id,
            proposal_id=v.proposal_id,
            vote_weights=json.loads(v.vote_weights),
            proof=v.proof,
        )
        for v in votes
    ]
