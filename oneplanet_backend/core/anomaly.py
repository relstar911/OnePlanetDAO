# anomaly.py – Datenmodell und Hilfsfunktionen für Anomaly Detection
from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class AnomalyLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    type: str  # z.B. "voting", "login", "kpi"
    description: str
    user_id: str | None = None
    severity: str = "low"  # "low", "medium", "high"
    resolved: bool = False


# Beispiel: Hilfsfunktion zum Anlegen eines AnomalyLog-Eintrags


def log_anomaly(
    session, type_: str, description: str, user_id: str | None = None, severity: str = "low"
):
    anomaly = AnomalyLog(
        type=type_,
        description=description,
        user_id=user_id,
        severity=severity,
        resolved=False,
    )
    session.add(anomaly)
    session.commit()
    return anomaly
