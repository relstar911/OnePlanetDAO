from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..core.db import get_session
from ..schemas.reporting import KPIResponse
from ..core.models import KPI, PrivacyClass
from ..core.privacy import audit_log_access
from typing import List, Optional
from fastapi import Query

router = APIRouter()


@router.post("/kpis", response_model=KPIResponse)
def create_kpi(kpi: KPIResponse, session: Session = Depends(get_session)):
    """
    KPI-Validierung:
    - Pflichtfelder: region, onRampSuccess, accessibilityScore,
      privacyShieldOptIn, empowermentKPI
    - Wertebereiche:
        onRampSuccess >=0, accessibilityScore 0-1,
        privacyShieldOptIn >=0, empowermentKPI >=0
    - region darf nicht leer sein
    """
    # Audit log: access to KPI creation
    audit_log_access(
        user_id="system",  # Optional: Hier kann bei späterem Auth-Feature der echte Nutzer
        model="KPI",
        model_id=kpi.region,
        action="POST /kpis",
        privacy_class=PrivacyClass.PUBLIC,
        reason="KPI submitted",
        session=session,
    )
    if (
        not kpi.region
        or kpi.onRampSuccess is None
        or kpi.accessibilityScore is None
        or kpi.privacyShieldOptIn is None
        or kpi.empowermentKPI is None
    ):
        detail_msg = (
            "Missing required KPI fields: region, onRampSuccess, accessibilityScore, "
            "privacyShieldOptIn, "
            "empowermentKPI"
        )
        raise HTTPException(status_code=400, detail=detail_msg)
    if not isinstance(kpi.region, str) or not kpi.region.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=("region muss ein nicht-leerer String sein."),
        )
    if not isinstance(kpi.onRampSuccess, int) or kpi.onRampSuccess < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="onRampSuccess muss >= 0 sein."
        )
    if not isinstance(kpi.accessibilityScore, float) or not (0.0 <= kpi.accessibilityScore <= 1.0):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=("accessibilityScore muss zwischen 0 und 1 liegen."),
        )
    if not isinstance(kpi.privacyShieldOptIn, int) or kpi.privacyShieldOptIn < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="privacyShieldOptIn muss >= 0 sein.",
        )
    if not isinstance(kpi.empowermentKPI, int) or kpi.empowermentKPI < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="empowermentKPI muss >= 0 sein.",
        )

    db_kpi = KPI(
        region=kpi.region,
        onRampSuccess=kpi.onRampSuccess,
        accessibilityScore=kpi.accessibilityScore,
        privacyShieldOptIn=kpi.privacyShieldOptIn,
        empowermentKPI=kpi.empowermentKPI,
    )
    session.add(db_kpi)
    session.commit()
    session.refresh(db_kpi)
    return KPIResponse(
        region=db_kpi.region,
        onRampSuccess=db_kpi.onRampSuccess,
        accessibilityScore=db_kpi.accessibilityScore,
        privacyShieldOptIn=db_kpi.privacyShieldOptIn,
        empowermentKPI=db_kpi.empowermentKPI,
    )


@router.get("/kpis", response_model=List[KPIResponse])
def list_kpis(region: Optional[str] = Query(None), session: Session = Depends(get_session)):
    if region:
        kpis = session.exec(select(KPI).where(KPI.region == region)).all()
    else:
        kpis = session.exec(select(KPI)).all()
    return [
        KPIResponse(
            region=k.region,
            onRampSuccess=k.onRampSuccess,
            accessibilityScore=k.accessibilityScore,
            privacyShieldOptIn=k.privacyShieldOptIn,
            empowermentKPI=k.empowermentKPI,
        )
        for k in kpis
    ]
