from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DeductionBase(BaseModel):
    name: str
    type: str
    amount: float
    description: Optional[str] = None
    payroll_id: Optional[int] = None


class DeductionCreate(DeductionBase):
    payroll_id: int


class DeductionResponse(DeductionBase):
    deduction_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
