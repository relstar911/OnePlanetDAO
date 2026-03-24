from pydantic import BaseModel


class KPIResponse(BaseModel):
    region: str
    epoch: int = 1
    participation_rate: float = 0.0
    accessibility_score: float = 0.0
    trust_index: float = 0.0
