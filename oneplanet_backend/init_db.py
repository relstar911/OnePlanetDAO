# init_db.py – Erstellt alle Tabellen in der Datenbank (inkl. AnomalyLog)
from sqlmodel import SQLModel
from oneplanet_backend.core.db import engine


if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)
    print("Alle Tabellen wurden erfolgreich erstellt (inkl. AnomalyLog und AuditLog).")
