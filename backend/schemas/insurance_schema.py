from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InsuranceBase(BaseModel):
    employee_id: int
    insurance_provider: str
    policy_number: str
    coverage_type: str
    premium_amount: float
    employer_contribution: Optional[float] = None
    employee_contribution: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None


class InsuranceCreate(InsuranceBase):
    pass


class InsuranceResponse(InsuranceBase):
    insurance_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}
