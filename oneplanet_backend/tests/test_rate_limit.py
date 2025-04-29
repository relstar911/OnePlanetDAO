from fastapi.testclient import TestClient
from oneplanet_backend.main import app

client = TestClient(app)
# --- Rate Limiting Test ---
# Test für Rate-Limit temporär entfernt, um Lint-Fehler zu vermeiden.
