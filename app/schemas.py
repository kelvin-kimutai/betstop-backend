from pydantic import BaseModel, constr
from datetime import datetime
from typing import Literal

class ExclusionCreate(BaseModel):
    mobile_number: constr(pattern=r"^\+2547\d{8}$")
    exclusion_period: Literal["6m", "1y", "5y"]

class ExclusionResponse(BaseModel):
    exclusion_id: str
    mobile_number: str
    exclusion_start: datetime
    exclusion_end: datetime
    status: str

    class Config:
        from_attributes = True