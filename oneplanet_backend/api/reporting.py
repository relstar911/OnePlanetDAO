from fastapi import APIRouter, Depends, Query
from ..schemas.reporting import KPIResponse
from ..core.db import get_session
from ..core.models import KPI
from sqlmodel import Session, select
from typing import List, Optional

router = APIRouter()

from fastapi import HTTPException, status

@router.post("/kpis", response_model=KPIResponse)
def create_kpi(kpi: KPIResponse, session: Session = Depends(get_session)):
    """
    KPI-Validierung:
    - Pflichtfelder: region, onRampSuccess, accessibilityScore, privacyShieldOptIn, empowermentKPI
    - Wertebereiche: onRampSuccess >=0, accessibilityScore 0-1, privacyShieldOptIn >=0, empowermentKPI >=0
    - region darf nicht leer sein
    """
    if not kpi.region or kpi.onRampSuccess is None or kpi.accessibilityScore is None or kpi.privacyShieldOptIn is None or kpi.empowermentKPI is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Alle Felder (region, onRampSuccess, accessibilityScore, privacyShieldOptIn, empowermentKPI) müssen gesetzt sein.")
    if not isinstance(kpi.region, str) or not kpi.region.strip():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="region muss ein nicht-leerer String sein.")
    if not isinstance(kpi.onRampSuccess, int) or kpi.onRampSuccess < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="onRampSuccess muss >= 0 sein.")
    if not isinstance(kpi.accessibilityScore, float) or not (0.0 <= kpi.accessibilityScore <= 1.0):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="accessibilityScore muss zwischen 0 und 1 liegen.")
    if not isinstance(kpi.privacyShieldOptIn, int) or kpi.privacyShieldOptIn < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="privacyShieldOptIn muss >= 0 sein.")
    if not isinstance(kpi.empowermentKPI, int) or kpi.empowermentKPI < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="empowermentKPI muss >= 0 sein.")

    db_kpi = KPI(
        region=kpi.region,
        onRampSuccess=kpi.onRampSuccess,
        accessibilityScore=kpi.accessibilityScore,
        privacyShieldOptIn=kpi.privacyShieldOptIn,
        empowermentKPI=kpi.empowermentKPI
    )
    session.add(db_kpi)
    session.commit()
    session.refresh(db_kpi)
    return KPIResponse(
        region=db_kpi.region,
        onRampSuccess=db_kpi.onRampSuccess,
        accessibilityScore=db_kpi.accessibilityScore,
        privacyShieldOptIn=db_kpi.privacyShieldOptIn,
        empowermentKPI=db_kpi.empowermentKPI
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
            empowermentKPI=k.empowermentKPI
        ) for k in kpis
    ]
