from fastapi import APIRouter, Depends
from ..schemas.identity import ProofRequest, ProofResponse, AppealRequest, AppealResponse
from ..core.db import get_session
from ..core.models import ProofRequest as ProofRequestModel
from sqlmodel import Session, select
from typing import List
import json

router = APIRouter()

@router.post("/proof-request", response_model=ProofResponse)
def proof_request(req: ProofRequest, session: Session = Depends(get_session)):
    """Process proof request for onboarding, recovery, voting."""
    db_proof = ProofRequestModel(
        user_id=req.user_id,
        proof_type=req.proof_type,
        public_signals=json.dumps(req.public_signals),
        external_nullifier=req.external_nullifier
    )
    session.add(db_proof)
    session.commit()
    session.refresh(db_proof)
    return ProofResponse(proof="<zk-proof-object>", status="success")

@router.get("/proof-requests", response_model=List[ProofRequest])
def list_proof_requests(session: Session = Depends(get_session)):
    proofs = session.exec(select(ProofRequestModel)).all()
    return [
        ProofRequest(
            user_id=p.user_id,
            proof_type=p.proof_type,
            public_signals=json.loads(p.public_signals),
            external_nullifier=p.external_nullifier
        ) for p in proofs
    ]

@router.post("/appeal", response_model=AppealResponse)
def appeal(req: AppealRequest):
    """Process appeal request."""
    return AppealResponse(status="pending", message="Appeal received.")
