from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.Insuarance_model import InsuranceStatus


class InsuranceBase(BaseModel):
    employee_id: int
    insurance_provider: str
    coverage_type: str
    premium_amount: float
    employer_contribution: Optional[float] = None
    employee_contribution: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status:InsuranceStatus = InsuranceStatus.ACTIVE 


class InsuranceCreate(InsuranceBase):
    pass


class InsuranceResponse(InsuranceBase):
    id: int
    start_date: Optional[datetime]
    end_date: Optional[datetime]

    model_config = {"from_attributes": True}
