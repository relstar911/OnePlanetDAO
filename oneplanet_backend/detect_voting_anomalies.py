# detect_voting_anomalies.py – Einfacher Detection-Task für Voting-Anomalien
from datetime import datetime, timedelta
from sqlmodel import Session, select
from oneplanet_backend.core.db import engine
from oneplanet_backend.core.anomaly import log_anomaly
from oneplanet_backend.core.privacy import AuditLog

# Regel: Mehr als 5 Votes eines Nutzers in weniger als 10 Minuten auf dasselbe Proposal = Anomalie
USER_VOTE_LIMIT = 5
TIME_WINDOW_MINUTES = 10


def detect_voting_anomalies():
    with Session(engine) as session:
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=TIME_WINDOW_MINUTES)
        # Finde alle Vote-Events im Zeitfenster
        vote_logs = session.exec(
            select(AuditLog)
            .where(AuditLog.action == "VOTE")
            .where(AuditLog.timestamp >= window_start)
        ).all()
        # Gruppiere nach user_id und proposal_id
        vote_map = {}
        for log in vote_logs:
            key = (log.user_id, log.model_id)  # model_id = proposal_id
            vote_map.setdefault(key, []).append(log)
        # Prüfe auf Überschreitung
        for (user_id, proposal_id), logs in vote_map.items():
            if len(logs) > USER_VOTE_LIMIT:
                description = (
                    f"User {user_id} voted {len(logs)} times on proposal "
                    f"{proposal_id} within {TIME_WINDOW_MINUTES} minutes."
                )
                log_anomaly(
                    session,
                    type_="voting",
                    description=description,
                    user_id=user_id,
                    severity="medium" if len(logs) <= USER_VOTE_LIMIT * 2 else "high",
                )
                print(f"Anomaly detected: {description}")


if __name__ == "__main__":
    detect_voting_anomalies()
