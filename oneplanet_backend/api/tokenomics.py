from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session, select
from ..core.auth import require_auth
from ..core.db import get_session
from ..schemas.tokenomics import AlertResponse
from ..core.models import Alert, PrivacyClass
from ..core.privacy import audit_log_access
from oneplanet_backend.core.limiter import limiter
from typing import List

router = APIRouter()


@router.post("/alerts", response_model=AlertResponse)
@limiter.limit("10/minute")
def create_alert(
    alert: AlertResponse,
    request: Request,
    session: Session = Depends(get_session),
    user=Depends(require_auth),
):
    """
    Alert-Validierung:
    - Pflichtfelder: epoch, msi, vei, collusion, status, alert
    - Wertebereiche: epoch >=0, msi/vei 0-1, collusion/status/alert nicht leer
    """
    # Audit log: access to alert creation
    audit_log_access(
        user_id=user["user_id"] if isinstance(user, dict) and "user_id" in user else str(user),
        model="Alert",
        model_id=str(alert.epoch),
        action="POST /alerts",
        privacy_class=PrivacyClass.PUBLIC,
        reason="Alert submitted",
        session=session,
    )
    if (
        alert.epoch is None
        or alert.msi is None
        or alert.vei is None
        or not alert.collusion
        or not alert.status
        or not alert.alert
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Alle Felder (epoch, msi, vei, collusion, status, alert) müssen gesetzt sein.",
        )
    if not isinstance(alert.epoch, int) or alert.epoch < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="epoch muss >= 0 sein."
        )
    if not isinstance(alert.msi, float) or not (0.0 <= alert.msi <= 1.0):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="msi muss zwischen 0 und 1 liegen.",
        )
    if not isinstance(alert.vei, float) or not (0.0 <= alert.vei <= 1.0):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="vei muss zwischen 0 und 1 liegen.",
        )
    for field in [alert.collusion, alert.status, alert.alert]:
        if not isinstance(field, str) or not field.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="collusion, status und alert müssen nicht-leere Strings sein.",
            )

    db_alert = Alert(
        epoch=alert.epoch,
        msi=alert.msi,
        vei=alert.vei,
        collusion=alert.collusion,
        status=alert.status,
        alert=alert.alert,
    )
    session.add(db_alert)
    session.commit()
    session.refresh(db_alert)
    return AlertResponse(
        epoch=db_alert.epoch,
        msi=db_alert.msi,
        vei=db_alert.vei,
        collusion=db_alert.collusion,
        status=db_alert.status,
        alert=db_alert.alert,
    )


@router.get("/alerts", response_model=List[AlertResponse])
def list_alerts(session: Session = Depends(get_session)):
    alerts = session.exec(select(Alert)).all()
    return [
        AlertResponse(
            epoch=a.epoch,
            msi=a.msi,
            vei=a.vei,
            collusion=a.collusion,
            status=a.status,
            alert=a.alert,
        )
        for a in alerts
    ]
