from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse
from oneplanet_backend.core.limiter import limiter
from slowapi import _rate_limit_exceeded_handler

from .api import governance, identity, tokenomics, reporting

app = FastAPI(
    title="One Planet Backend",
    description="API for One Planet governance, identity, tokenomics, and reporting, strictly aligned with project documentation in /docs.",
    version="0.1.0"
)

# Rate Limiting: 10 req/min per IP (POST/PUT/DELETE)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.exception_handler(RateLimitExceeded)
async def ratelimit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Bitte warte einen Moment und versuche es erneut."}
    )

# Routers (activated per docs)
from .api import governance, identity, tokenomics, reporting
app.include_router(governance.router, prefix="/api/governance")
app.include_router(identity.router, prefix="/api/identity")
app.include_router(tokenomics.router, prefix="/api/tokenomics")
app.include_router(reporting.router, prefix="/api/reporting")

@app.get("/")
def root():
    return {"msg": "Welcome to the One Planet API. See /docs for OpenAPI and project documentation."}
