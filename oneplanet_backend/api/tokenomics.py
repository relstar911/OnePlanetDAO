from fastapi import APIRouter
from ..schemas.tokenomics import AlertResponse

router = APIRouter()

@router.get("/alerts", response_model=AlertResponse)
def get_alerts():
    """Get real-time tokenomics alerts (MSI, VEI, Collusion)."""
    # Dummy data, see Tokenomics & Soul-Credits dashboard mockup
    return AlertResponse(
        epoch=113,
        msi=0.59,
        vei=0.21,
        collusion="Bloc",
        status="Collusion Alert",
        alert="Push Sent"
    )
