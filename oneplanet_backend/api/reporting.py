from fastapi import APIRouter
from ..schemas.reporting import KPIResponse

router = APIRouter()

@router.get("/reporting/kpis", response_model=KPIResponse)
def get_kpis(region: str):
    """Get reporting KPIs for a region (see System Blueprint/Reporting API)."""
    # Dummy data for now
    return KPIResponse(
        region=region,
        onRampSuccess=88,
        accessibilityScore=0.92,
        privacyShieldOptIn=7,
        empowermentKPI=5
    )
