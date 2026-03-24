"""
Central configuration for the OnePlanet backend.
All secrets and environment-specific settings are loaded from environment
variables (with .env support via python-dotenv).
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env file from project root if it exists
_env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(_env_path)


# --- JWT ---
JWT_SECRET: str = os.environ.get("ONEPLANET_JWT_SECRET", "")
JWT_ALGORITHM: str = os.environ.get("ONEPLANET_JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES: int = int(os.environ.get("ONEPLANET_JWT_EXPIRE_MINUTES", "60"))

if not JWT_SECRET:
    import warnings

    warnings.warn(
        "ONEPLANET_JWT_SECRET is not set! Using an insecure default. "
        "Set it in your .env file or environment for production.",
        stacklevel=2,
    )
    JWT_SECRET = "insecure-dev-secret-do-not-use-in-production"

# --- Database ---
DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite:///./oneplanet.db")

# --- Rate Limiting ---
RATE_LIMIT_DEFAULT: str = os.environ.get("RATE_LIMIT_DEFAULT", "100/minute")
RATE_LIMIT_STRICT: str = os.environ.get("RATE_LIMIT_STRICT", "10/minute")

# --- Environment ---
ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "development")
TESTING: bool = os.environ.get("TESTING", "0") == "1"

# --- Logging ---
LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")
