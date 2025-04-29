from fastapi import APIRouter, Depends
from ..schemas.identity import ProofRequest, ProofResponse, AppealRequest, AppealResponse
from ..core.db import get_session
from ..core.models import ProofRequest as ProofRequestModel
from sqlmodel import Session, select
from typing import List
import json

router = APIRouter()

from fastapi import HTTPException, status

@router.post("/proof-request", response_model=ProofResponse)
def proof_request(req: ProofRequest, session: Session = Depends(get_session)):
    """
    Process proof request for onboarding, recovery, voting.
    Validierung:
    - Pflichtfelder: user_id, proof_type, public_signals, external_nullifier
    - proof_type: nur bestimmte Werte erlaubt
    - public_signals: nicht-leere Liste
    - external_nullifier: nicht leer, String
    """
    ALLOWED_PROOF_TYPES = {"onboarding", "recovery", "voting"}
    if not req.user_id or not req.proof_type or req.public_signals is None or not req.external_nullifier:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Alle Felder (user_id, proof_type, public_signals, external_nullifier) müssen gesetzt sein.")
    if req.proof_type not in ALLOWED_PROOF_TYPES:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"proof_type muss einer der erlaubten Werte sein: {ALLOWED_PROOF_TYPES}")
    if not isinstance(req.public_signals, list) or not req.public_signals:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="public_signals muss eine nicht-leere Liste sein.")
    if not isinstance(req.external_nullifier, str) or not req.external_nullifier.strip():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="external_nullifier darf nicht leer sein und muss ein String sein.")

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
