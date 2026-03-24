from pydantic import BaseModel


class AlertResponse(BaseModel):
    epoch: int
    msi: float
    vei: float
    collusion_flag: bool = False
    status: str
