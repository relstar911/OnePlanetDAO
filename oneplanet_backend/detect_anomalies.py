# detect_anomalies.py – Erweiterte Detection für verschiedene Anomalie-Typen
from datetime import datetime, timedelta
from sqlmodel import Session, select
from oneplanet_backend.core.db import engine
from oneplanet_backend.core.anomaly import log_anomaly
from oneplanet_backend.core.privacy import AuditLog

# Voting-Anomalie: Mehr als 5 Votes pro Proposal/Nutzer in 10 Min
VOTE_LIMIT = 5
VOTE_WINDOW_MIN = 10

# Login-Anomalie: Mehr als 3 fehlgeschlagene Logins pro Nutzer in 5 Min
LOGIN_FAIL_LIMIT = 3
LOGIN_WINDOW_MIN = 5

# KPI-Anomalie: KPI-Werte außerhalb plausibler Grenzen (Beispiel: empowermentKPI < 0 oder > 100)
KPI_MIN = 0
KPI_MAX = 100


def detect_voting_anomalies(session):
    now = datetime.utcnow()
    window_start = now - timedelta(minutes=VOTE_WINDOW_MIN)
    vote_logs = session.exec(
        select(AuditLog).where(AuditLog.action == "VOTE").where(AuditLog.timestamp >= window_start)
    ).all()
    vote_map = {}
    for log in vote_logs:
        key = (log.user_id, log.model_id)
        vote_map.setdefault(key, []).append(log)
    for (user_id, proposal_id), logs in vote_map.items():
        if len(logs) > VOTE_LIMIT:
            description = (
                f"User {user_id} voted {len(logs)} times on proposal {proposal_id} "
                f"within {VOTE_WINDOW_MIN} minutes."
            )
            log_anomaly(
                session,
                type_="voting",
                description=description,
                user_id=user_id,
                severity="medium" if len(logs) <= VOTE_LIMIT * 2 else "high",
            )
            print(f"Anomaly detected: {description}")


def detect_login_anomalies(session):
    now = datetime.utcnow()
    window_start = now - timedelta(minutes=LOGIN_WINDOW_MIN)
    fail_logs = session.exec(
        select(AuditLog)
        .where(AuditLog.action == "LOGIN_FAIL")
        .where(AuditLog.timestamp >= window_start)
    ).all()
    fail_map = {}
    for log in fail_logs:
        key = log.user_id
        fail_map.setdefault(key, []).append(log)
    for user_id, logs in fail_map.items():
        if len(logs) > LOGIN_FAIL_LIMIT:
            description = (
                f"User {user_id} had {len(logs)} failed logins within {LOGIN_WINDOW_MIN} minutes."
            )
            log_anomaly(
                session,
                type_="login",
                description=description,
                user_id=user_id,
                severity="medium" if len(logs) <= LOGIN_FAIL_LIMIT * 2 else "high",
            )
            print(f"Anomaly detected: {description}")


def detect_kpi_anomalies(session):
    # Beispiel: EmpowermentKPI außerhalb [0, 100] (hier als AuditLog-Reason gespeichert)
    kpi_logs = session.exec(select(AuditLog).where(AuditLog.action == "KPI_REPORT")).all()
    for log in kpi_logs:
        try:
            # Annahme: KPI-Wert steht als Zahl im reason-Feld
            kpi_value = float(log.reason)
            if kpi_value < KPI_MIN or kpi_value > KPI_MAX:
                description = (
                    f"KPI value {kpi_value} for user {log.user_id} outside plausible range "
                    f"[{KPI_MIN}, {KPI_MAX}]."
                )
                log_anomaly(
                    session,
                    type_="kpi",
                    description=description,
                    user_id=log.user_id,
                    severity="medium" if kpi_value < KPI_MIN or kpi_value > KPI_MAX else "low",
                )
                print(f"Anomaly detected: {description}")
        except Exception:
            continue


def detect_all_anomalies():
    with Session(engine) as session:
        detect_voting_anomalies(session)
        detect_login_anomalies(session)
        detect_kpi_anomalies(session)


if __name__ == "__main__":
    detect_all_anomalies()
