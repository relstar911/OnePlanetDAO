import json
import time

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session, select

from ..core.auth import create_access_token, hash_password, require_auth, verify_password
from ..core.db import get_session
from ..core.limiter import limiter
from ..core.models import PrivacyClass, User
from ..core.models import ProofRequest as ProofRequestModel
from ..core.privacy import audit_log_access
from ..schemas.identity import (
    AppealRequest,
    AppealResponse,
    LoginRequest,
    ProofRequest,
    ProofResponse,
    RegisterRequest,
)

router = APIRouter()


@router.post("/proof-request", response_model=ProofResponse)
@limiter.limit("10/minute")
def proof_request(
    req: ProofRequest,
    request: Request,
    session: Session = Depends(get_session),  # noqa: B008
    user=Depends(require_auth),  # noqa: B008
):
    """
    Process proof request for onboarding, recovery, voting.
    Validierung:
    - Pflichtfelder: user_id, proof_type, public_signals, external_nullifier
    - proof_type: nur bestimmte Werte erlaubt
    - public_signals: nicht-leere Liste
    - external_nullifier: nicht leer, String
    """
    ALLOWED_PROOF_TYPES = {"onboarding", "recovery", "voting"}
    # Audit log: access to sensitive proof request
    audit_log_access(
        user_id=user["user_id"] if isinstance(user, dict) and "user_id" in user else str(user),
        model="ProofRequest",
        model_id=req.user_id,
        action="POST /proof-request",
        privacy_class=PrivacyClass.MEMBER_ONLY,
        reason="ProofRequest submitted",
        session=session,
    )
    if (
        not req.user_id
        or not req.proof_type
        or req.public_signals is None
        or not req.external_nullifier
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "Alle Felder (user_id, proof_type, public_signals, "
                "external_nullifier) müssen gesetzt sein."
            ),
        )
    if req.proof_type not in ALLOWED_PROOF_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(f"proof_type muss einer der erlaubten Werte sein: {ALLOWED_PROOF_TYPES}"),
        )
    if not isinstance(req.public_signals, list) or not req.public_signals:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="public_signals muss eine nicht-leere Liste sein.",
        )
    if not isinstance(req.external_nullifier, str) or not req.external_nullifier.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="external_nullifier darf nicht leer sein und muss ein String sein.",
        )

    db_proof = ProofRequestModel(
        user_id=req.user_id,
        proof_type=req.proof_type,
        public_signals=json.dumps(req.public_signals),
        external_nullifier=req.external_nullifier,
    )
    session.add(db_proof)
    session.commit()
    session.refresh(db_proof)
    return ProofResponse(proof="<zk-proof-object>", status="success")


@router.get("/proof-requests", response_model=list[ProofRequest])
def list_proof_requests(session: Session = Depends(get_session)):  # noqa: B008
    proofs = session.exec(select(ProofRequestModel)).all()
    return [
        ProofRequest(
            user_id=p.user_id,
            proof_type=p.proof_type,
            public_signals=json.loads(p.public_signals),
            external_nullifier=p.external_nullifier,
        )
        for p in proofs
    ]


@router.post("/appeal", response_model=AppealResponse)
@limiter.limit("10/minute")
def appeal(
    req: AppealRequest,
    request: Request,
    user=Depends(require_auth),  # noqa: B008
):
    """Process appeal request."""
    case_id = f"{req.user_id}-{int(time.time())}"
    return AppealResponse(status="pending", case_id=case_id)


@router.post("/register")
@limiter.limit("5/minute")
def register(
    data: RegisterRequest,
    request: Request,
    session: Session = Depends(get_session),  # noqa: B008
):
    """Register a new user with user_id and password."""
    if not data.user_id or not data.user_id.strip():
        raise HTTPException(status_code=400, detail="user_id required")
    if not data.password or len(data.password) < 4:
        raise HTTPException(status_code=400, detail="Password must be at least 4 characters")

    existing = session.exec(select(User).where(User.user_id == data.user_id)).first()
    if existing:
        raise HTTPException(status_code=409, detail="User already exists")

    user = User(
        user_id=data.user_id,
        password_hash=hash_password(data.password),
        region=data.region,
    )
    session.add(user)
    session.commit()

    access_token = create_access_token({"user_id": data.user_id})
    return {"access_token": access_token, "token_type": "bearer", "user_id": data.user_id}


@router.post("/login")
@limiter.limit("10/minute")
def login(
    data: LoginRequest,
    request: Request,
    session: Session = Depends(get_session),  # noqa: B008
):
    """Authenticate user with user_id and password."""
    if not data.user_id:
        raise HTTPException(status_code=400, detail="user_id required")
    if not data.password:
        raise HTTPException(status_code=400, detail="password required")

    user = session.exec(select(User).where(User.user_id == data.user_id)).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"user_id": data.user_id})
    return {"access_token": access_token, "token_type": "bearer"}
