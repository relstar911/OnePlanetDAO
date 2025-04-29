from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List, Optional
from ..core.db import get_session
from ..core.anomaly import AnomalyLog

router = APIRouter()


@router.get("/anomalies", response_model=List[AnomalyLog])
def list_anomalies(
    resolved: Optional[bool] = None,
    type: Optional[str] = None,
    user_id: Optional[str] = None,
    session: Session = Depends(get_session),
):
    query = select(AnomalyLog)
    if resolved is not None:
        query = query.where(AnomalyLog.resolved == resolved)
    if type:
        query = query.where(AnomalyLog.type == type)
    if user_id:
        query = query.where(AnomalyLog.user_id == user_id)
    anomalies = session.exec(query.order_by(AnomalyLog.timestamp.desc())).all()
    return anomalies
