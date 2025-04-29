from fastapi import FastAPI

from .api import governance, identity, tokenomics, reporting

app = FastAPI(
    title="One Planet Backend",
    description="API for One Planet governance, identity, tokenomics, and reporting, strictly aligned with project documentation in /docs.",
    version="0.1.0"
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
