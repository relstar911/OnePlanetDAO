from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlmodel import SQLModel
from starlette.responses import JSONResponse

import oneplanet_backend.core.anomaly  # noqa: F401

# Import all models so SQLModel.metadata knows about them
import oneplanet_backend.core.models  # noqa: F401
import oneplanet_backend.core.privacy  # noqa: F401
import oneplanet_backend.core.recovery  # noqa: F401
from oneplanet_backend.api import (
    anomaly,
    governance,
    identity,
    recovery,
    reporting,
    seed,
    tokenomics,
)
from oneplanet_backend.core.config import ALLOWED_ORIGINS, ENVIRONMENT
from oneplanet_backend.core.db import engine
from oneplanet_backend.core.limiter import limiter


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="One Planet Backend",
    description=(
        "API for One Planet governance, identity, tokenomics, and reporting. "
        "A supranational governance platform for global citizens."
    ),
    version="0.2.0",
    lifespan=lifespan,
)

# CORS – allow frontend origins
_dev_origins = ["http://localhost:3000", "http://localhost:5173"]
_cors_origins = _dev_origins + ALLOWED_ORIGINS if ENVIRONMENT == "development" else ALLOWED_ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.exception_handler(RateLimitExceeded)
async def ratelimit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please wait a moment and try again."},
    )


app.include_router(governance.router, prefix="/api/governance", tags=["Governance"])
app.include_router(identity.router, prefix="/api/identity", tags=["Identity"])
app.include_router(tokenomics.router, prefix="/api/tokenomics", tags=["Tokenomics"])
app.include_router(reporting.router, prefix="/api/reporting", tags=["Reporting"])
app.include_router(anomaly.router, prefix="/api/anomaly", tags=["Anomaly Detection"])
app.include_router(recovery.router, prefix="/api/identity", tags=["Recovery"])
app.include_router(seed.router, prefix="/api/dev", tags=["Development"])


@app.get("/", tags=["Health"])
def root():
    return {
        "name": "One Planet API",
        "version": "0.2.0",
        "status": "running",
        "docs": "/docs",
        "environment": ENVIRONMENT,
    }
