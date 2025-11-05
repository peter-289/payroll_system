from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PensionBase(BaseModel):
    employee_id: int
    scheme_name: Optional[str] = None
    pension_number: Optional[int] = None
    employer_contribution_percentage: Optional[float] = None
    employee_contribution_percentage: Optional[float] = None
    monthly_contribution: Optional[float] = None


class PensionCreate(PensionBase):
    pass


class PensionResponse(PensionBase):
    pension_id: int
    start_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
