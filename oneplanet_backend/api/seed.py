"""
Seed endpoint – populates the database with demo data for development and demos.
Only available when ENVIRONMENT != 'production'.
"""

import json

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..core.anomaly import AnomalyLog
from ..core.auth import hash_password
from ..core.config import ENVIRONMENT
from ..core.db import get_session
from ..core.models import KPI, Alert, User, Vote

router = APIRouter()

DEMO_USERS = [
    {"user_id": "alice", "password": "alice1234", "region": "Europe"},
    {"user_id": "bob", "password": "bob1234", "region": "Europe"},
    {"user_id": "carol", "password": "carol1234", "region": "East Africa"},
    {"user_id": "david", "password": "david1234", "region": "South America"},
    {"user_id": "eve", "password": "eve1234", "region": "Southeast Asia"},
    {"user_id": "frank", "password": "frank1234", "region": "North America"},
    {"user_id": "grace", "password": "grace1234", "region": "North America"},
]


DEMO_VOTES = [
    {
        "user_id": "alice",
        "proposal_id": "climate-fund-2026",
        "vote_weights": {"climate": 3, "adaptation": 1},
        "proof": "zk-proof-alice",
    },
    {
        "user_id": "bob",
        "proposal_id": "climate-fund-2026",
        "vote_weights": {"climate": 2, "adaptation": 2},
        "proof": "zk-proof-bob",
    },
    {
        "user_id": "carol",
        "proposal_id": "education-global",
        "vote_weights": {"access": 1},
        "proof": "zk-proof-carol",
    },
    {
        "user_id": "david",
        "proposal_id": "climate-fund-2026",
        "vote_weights": {"climate": 4},
        "proof": "zk-proof-david",
    },
    {
        "user_id": "eve",
        "proposal_id": "health-access-2026",
        "vote_weights": {"vaccines": 2, "infrastructure": 3},
        "proof": "zk-proof-eve",
    },
    {
        "user_id": "frank",
        "proposal_id": "education-global",
        "vote_weights": {"access": 1, "teachers": 1, "materials": 1},
        "proof": "zk-proof-frank",
    },
    {
        "user_id": "grace",
        "proposal_id": "health-access-2026",
        "vote_weights": {"vaccines": 5},
        "proof": "zk-proof-grace",
    },
]

DEMO_KPIS = [
    {
        "region": "Europe",
        "epoch": 1,
        "participation_rate": 72.5,
        "accessibility_score": 88.0,
        "trust_index": 0.91,
    },
    {
        "region": "East Africa",
        "epoch": 1,
        "participation_rate": 45.2,
        "accessibility_score": 61.0,
        "trust_index": 0.78,
    },
    {
        "region": "South America",
        "epoch": 1,
        "participation_rate": 58.7,
        "accessibility_score": 74.0,
        "trust_index": 0.84,
    },
    {
        "region": "Southeast Asia",
        "epoch": 1,
        "participation_rate": 63.1,
        "accessibility_score": 69.0,
        "trust_index": 0.82,
    },
    {
        "region": "North America",
        "epoch": 1,
        "participation_rate": 68.9,
        "accessibility_score": 92.0,
        "trust_index": 0.89,
    },
]

DEMO_ALERTS = [
    {"epoch": 1, "msi": 0.15, "vei": 0.82, "collusion_flag": False, "status": "active"},
    {"epoch": 1, "msi": 0.67, "vei": 0.41, "collusion_flag": True, "status": "active"},
    {"epoch": 2, "msi": 0.08, "vei": 0.91, "collusion_flag": False, "status": "resolved"},
]

DEMO_ANOMALIES = [
    {
        "type": "voting",
        "description": "Unusual voting pattern: 5 votes from same IP range in 2 minutes",
        "user_id": "unknown-ip-cluster",
        "severity": "medium",
        "resolved": False,
    },
    {
        "type": "login",
        "description": "Brute-force attempt detected: 50 failed logins for user_id 'admin'",
        "user_id": "admin",
        "severity": "high",
        "resolved": True,
    },
    {
        "type": "kpi",
        "description": "Participation rate dropped 30% in East Africa region",
        "user_id": None,
        "severity": "low",
        "resolved": False,
    },
]


@router.post("/seed")
def seed_demo_data(session: Session = Depends(get_session)):  # noqa: B008
    if ENVIRONMENT == "production":
        return {"detail": "Seed endpoint is disabled in production."}

    # Check if already seeded
    existing = session.exec(select(User)).first()
    if existing:
        return {"detail": "Database already contains data. Skipping seed.", "seeded": False}

    # Seed users with hashed passwords
    for u in DEMO_USERS:
        session.add(
            User(
                user_id=u["user_id"],
                password_hash=hash_password(u["password"]),
                region=u["region"],
            )
        )

    # Seed votes (vote_weights must be JSON-encoded for the model)
    for v in DEMO_VOTES:
        vote_data = {**v, "vote_weights": json.dumps(v["vote_weights"])}
        session.add(Vote(**vote_data))

    # Seed KPIs
    for k in DEMO_KPIS:
        session.add(KPI(**k))

    # Seed alerts
    for a in DEMO_ALERTS:
        session.add(Alert(**a))

    # Seed anomalies
    for an in DEMO_ANOMALIES:
        session.add(AnomalyLog(**an))

    session.commit()

    return {
        "detail": "Demo data seeded successfully.",
        "seeded": True,
        "counts": {
            "users": len(DEMO_USERS),
            "votes": len(DEMO_VOTES),
            "kpis": len(DEMO_KPIS),
            "alerts": len(DEMO_ALERTS),
            "anomalies": len(DEMO_ANOMALIES),
        },
    }
