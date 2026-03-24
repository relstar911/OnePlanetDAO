from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlmodel import Session, select

from ..core.db import get_session
from ..core.i18n import get_error_message, get_locale
from ..core.models import KPI, PrivacyClass
from ..core.privacy import audit_log_access
from ..schemas.reporting import KPIResponse

router = APIRouter()


@router.post("/kpis", response_model=KPIResponse)
def create_kpi(
    kpi: KPIResponse,
    request: Request,
    session: Session = Depends(get_session),  # noqa: B008
):
    """
    KPI-Validierung:
    - Pflichtfelder: region, epoch, participation_rate, accessibility_score, trust_index
    - Wertebereiche:
        epoch >= 0, participation_rate 0-100,
        accessibility_score 0-100, trust_index 0-1
    - region darf nicht leer sein
    """
    # Audit log: access to KPI creation
    audit_log_access(
        user_id="system",
        model="KPI",
        model_id=kpi.region,
        action="POST /kpis",
        privacy_class=PrivacyClass.PUBLIC,
        reason="KPI submitted",
        session=session,
    )
    if not kpi.region:
        locale = get_locale(request)
        detail_msg = get_error_message("missing_kpi_fields", locale)
        raise HTTPException(status_code=400, detail=detail_msg)
    if not isinstance(kpi.region, str) or not kpi.region.strip():
        locale = get_locale(request)
        detail_msg = get_error_message("invalid_region", locale)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail_msg,
        )
    if not isinstance(kpi.participation_rate, int | float) or not (
        0.0 <= kpi.participation_rate <= 100.0
    ):
        locale = get_locale(request)
        detail_msg = get_error_message("invalid_participation_rate", locale)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail_msg,
        )
    if not isinstance(kpi.accessibility_score, int | float) or not (
        0.0 <= kpi.accessibility_score <= 100.0
    ):
        locale = get_locale(request)
        detail_msg = get_error_message("invalid_accessibility_score", locale)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail_msg,
        )
    if not isinstance(kpi.trust_index, int | float) or not (0.0 <= kpi.trust_index <= 1.0):
        locale = get_locale(request)
        detail_msg = get_error_message("invalid_trust_index", locale)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail_msg,
        )

    db_kpi = KPI(
        region=kpi.region,
        epoch=kpi.epoch,
        participation_rate=kpi.participation_rate,
        accessibility_score=kpi.accessibility_score,
        trust_index=kpi.trust_index,
    )
    session.add(db_kpi)
    session.commit()
    session.refresh(db_kpi)
    return KPIResponse(
        region=db_kpi.region,
        epoch=db_kpi.epoch,
        participation_rate=db_kpi.participation_rate,
        accessibility_score=db_kpi.accessibility_score,
        trust_index=db_kpi.trust_index,
    )


@router.get("/kpis", response_model=list[KPIResponse])
def list_kpis(
    region: str | None = Query(None),  # noqa: B008
    session: Session = Depends(get_session),  # noqa: B008
):
    if region:
        kpis = session.exec(select(KPI).where(KPI.region == region)).all()
    else:
        kpis = session.exec(select(KPI)).all()
    return [
        KPIResponse(
            region=k.region,
            epoch=k.epoch,
            participation_rate=k.participation_rate,
            accessibility_score=k.accessibility_score,
            trust_index=k.trust_index,
        )
        for k in kpis
    ]
