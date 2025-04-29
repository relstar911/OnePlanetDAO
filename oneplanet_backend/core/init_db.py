from sqlmodel import SQLModel
from .db import engine
from .models import User, Proposal, Vote, ProofRequest, Alert, KPI

def init_db():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
    print("DB tables created.")
