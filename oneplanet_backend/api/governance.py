import json

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session, select

from ..core.auth import require_auth
from ..core.db import get_session
from ..core.limiter import limiter
from ..core.models import PrivacyClass, Proposal, Vote
from ..core.privacy import audit_log_access
from ..schemas.governance import ProposalCreate, ProposalResponse, VoteRequest, VoteResponse
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


# --- Proposals ---


@router.post("/proposals", response_model=ProposalResponse)
@limiter.limit("10/minute")
def create_proposal(
    data: ProposalCreate,
    request: Request,
    session: Session = Depends(get_session),  # noqa: B008
    user=Depends(require_auth),  # noqa: B008
):
    """Create a new proposal."""
    if not data.proposal_id or not data.proposal_id.strip():
        raise HTTPException(status_code=400, detail="proposal_id required")
    if not data.title or not data.title.strip():
        raise HTTPException(status_code=400, detail="title required")

    existing = session.exec(
        select(Proposal).where(Proposal.proposal_id == data.proposal_id)
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Proposal ID already exists")

    db_proposal = Proposal(
        proposal_id=data.proposal_id,
        title=data.title,
        description=data.description,
    )
    session.add(db_proposal)
    session.commit()
    session.refresh(db_proposal)
    return ProposalResponse(
        id=db_proposal.id,
        proposal_id=db_proposal.proposal_id,
        title=db_proposal.title,
        description=db_proposal.description,
    )


@router.get("/proposals", response_model=list[ProposalResponse])
def list_proposals(session: Session = Depends(get_session)):  # noqa: B008
    proposals = session.exec(select(Proposal)).all()
    return [
        ProposalResponse(
            id=p.id,
            proposal_id=p.proposal_id,
            title=p.title,
            description=p.description,
        )
        for p in proposals
    ]
