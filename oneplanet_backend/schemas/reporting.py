from pydantic import BaseModel

class KPIResponse(BaseModel):
    region: str
    onRampSuccess: int
    accessibilityScore: float
    privacyShieldOptIn: int
    empowermentKPI: int
