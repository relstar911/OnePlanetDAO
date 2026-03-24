from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session, select

from oneplanet_backend.core.limiter import limiter

from ..core.auth import require_auth
from ..core.db import get_session
from ..core.models import Alert, PrivacyClass
from ..core.privacy import audit_log_access
from ..schemas.tokenomics import AlertResponse

router = APIRouter()


@router.post("/alerts", response_model=AlertResponse)
@limiter.limit("10/minute")
def create_alert(
    alert: AlertResponse,
    request: Request,
    session: Session = Depends(get_session),  # noqa: B008
    user=Depends(require_auth),  # noqa: B008
):
    """
    Alert-Validierung:
    - Pflichtfelder: epoch, msi, vei, collusion_flag, status
    - Wertebereiche: epoch >=0, msi/vei 0-1, collusion_flag bool, status nicht leer
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
    if alert.epoch is None or alert.msi is None or alert.vei is None or not alert.status:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Alle Felder (epoch, msi, vei, collusion_flag, status) müssen gesetzt sein.",
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
    if not isinstance(alert.status, str) or not alert.status.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="status muss ein nicht-leerer String sein.",
        )

    db_alert = Alert(
        epoch=alert.epoch,
        msi=alert.msi,
        vei=alert.vei,
        collusion_flag=alert.collusion_flag,
        status=alert.status,
    )
    session.add(db_alert)
    session.commit()
    session.refresh(db_alert)
    return AlertResponse(
        epoch=db_alert.epoch,
        msi=db_alert.msi,
        vei=db_alert.vei,
        collusion_flag=db_alert.collusion_flag,
        status=db_alert.status,
    )


@router.get("/alerts", response_model=list[AlertResponse])
def list_alerts(session: Session = Depends(get_session)):  # noqa: B008
    alerts = session.exec(select(Alert)).all()
    return [
        AlertResponse(
            epoch=a.epoch,
            msi=a.msi,
            vei=a.vei,
            collusion_flag=a.collusion_flag,
            status=a.status,
        )
        for a in alerts
    ]
