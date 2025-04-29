from pydantic import BaseModel


class AlertResponse(BaseModel):
    epoch: int
    msi: float
    vei: float
    collusion: str
    status: str
    alert: str
