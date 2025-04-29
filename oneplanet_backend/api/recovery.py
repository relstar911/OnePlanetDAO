from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.attributes import flag_modified
from sqlmodel import Session, select
from ..core.db import get_session
from ..core.recovery import GuardianAssignment, RecoveryRequest
from ..core.privacy import audit_log_access, PrivacyClass

router = APIRouter()


@router.post("/guardians", response_model=GuardianAssignment)
def add_guardian(user_id: str, guardian_id: str, session: Session = Depends(get_session)):
    # Prüfe, ob Guardian schon zugeordnet
    existing = session.exec(
        select(GuardianAssignment).where(
            GuardianAssignment.user_id == user_id,
            GuardianAssignment.guardian_id == guardian_id,
            GuardianAssignment.status == "active",
        )
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Guardian already assigned.")
    assignment = GuardianAssignment(user_id=user_id, guardian_id=guardian_id)
    session.add(assignment)
    session.commit()
    audit_log_access(
        user_id=user_id,
        model="GuardianAssignment",
        model_id=str(assignment.id),
        action="ADD_GUARDIAN",
        privacy_class=PrivacyClass.MEMBER_ONLY,
        reason=f"Added guardian {guardian_id}",
        session=session,
    )
    return {
        "user_id": assignment.user_id,
        "guardian_id": assignment.guardian_id,
        "status": assignment.status,
    }


@router.delete("/guardians", response_model=dict)
def remove_guardian(user_id: str, guardian_id: str, session: Session = Depends(get_session)):
    assignment = session.exec(
        select(GuardianAssignment).where(
            GuardianAssignment.user_id == user_id,
            GuardianAssignment.guardian_id == guardian_id,
            GuardianAssignment.status == "active",
        )
    ).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Guardian not found.")
    assignment.status = "revoked"
    session.add(assignment)
    session.commit()
    audit_log_access(
        user_id=user_id,
        model="GuardianAssignment",
        model_id=str(assignment.id),
        action="REMOVE_GUARDIAN",
        privacy_class=PrivacyClass.MEMBER_ONLY,
        reason=f"Revoked guardian {guardian_id}",
        session=session,
    )
    return {"msg": "Guardian revoked."}


@router.post("/recovery-request", response_model=RecoveryRequest)
def start_recovery(
    user_id: str, initiator_id: str, threshold: int = 2, session: Session = Depends(get_session)
):
    req = RecoveryRequest(
        user_id=user_id, initiator_id=initiator_id, threshold=threshold, approvals=[]
    )
    session.add(req)
    session.commit()
    audit_log_access(
        user_id=initiator_id,
        model="RecoveryRequest",
        model_id=str(req.id),
        action="START_RECOVERY",
        privacy_class=PrivacyClass.MEMBER_ONLY,
        reason=f"Started recovery for {user_id}",
        session=session,
    )
    return {
        "id": req.id,
        "user_id": req.user_id,
        "initiator_id": req.initiator_id,
        "status": req.status,
        "approvals": req.approvals,
        "threshold": req.threshold,
    }


@router.post("/recovery-approve", response_model=RecoveryRequest)
def approve_recovery(request_id: int, guardian_id: str, session: Session = Depends(get_session)):
    req = session.get(RecoveryRequest, request_id)
    if not req or req.status in ("denied", "completed"):
        raise HTTPException(status_code=404, detail="Recovery request not found or not pending.")
    if guardian_id in req.approvals:
        raise HTTPException(status_code=400, detail="Guardian already approved.")
    req.approvals.append(guardian_id)
    flag_modified(req, "approvals")
    # Schwelle erreicht? (Status bleibt approved, weitere Approvals möglich)
    if req.status == "pending" and len(req.approvals) >= req.threshold:
        req.status = "approved"
    session.add(req)
    session.commit()
    session.refresh(req)
    audit_log_access(
        user_id=guardian_id,
        model="RecoveryRequest",
        model_id=str(req.id),
        action="APPROVE_RECOVERY",
        privacy_class=PrivacyClass.MEMBER_ONLY,
        reason=f"Guardian {guardian_id} approved recovery.",
        session=session,
    )
    return {
        "id": req.id,
        "user_id": req.user_id,
        "initiator_id": req.initiator_id,
        "status": req.status,
        "approvals": req.approvals,
        "threshold": req.threshold,
    }


@router.get("/recovery-status", response_model=RecoveryRequest)
def get_recovery_status(request_id: int, session: Session = Depends(get_session)):
    req = session.get(RecoveryRequest, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Recovery request not found.")
    return {
        "id": req.id,
        "user_id": req.user_id,
        "initiator_id": req.initiator_id,
        "status": req.status,
        "approvals": req.approvals,
        "threshold": req.threshold,
    }


@router.post("/recovery-deny", response_model=RecoveryRequest)
def deny_recovery(
    request_id: int, denier_id: str, reason: str = "", session: Session = Depends(get_session)
):
    req = session.get(RecoveryRequest, request_id)
    if not req or req.status in ("denied", "completed"):
        raise HTTPException(
            status_code=404, detail="Recovery request not found or already denied/completed."
        )
    req.status = "denied"
    session.add(req)
    session.commit()
    session.refresh(req)
    audit_log_access(
        user_id=denier_id,
        model="RecoveryRequest",
        model_id=str(req.id),
        action="DENY_RECOVERY",
        privacy_class=PrivacyClass.MEMBER_ONLY,
        reason=reason or f"Recovery denied by {denier_id}",
        session=session,
    )
    return {
        "id": req.id,
        "user_id": req.user_id,
        "initiator_id": req.initiator_id,
        "status": req.status,
        "approvals": req.approvals,
        "threshold": req.threshold,
    }
