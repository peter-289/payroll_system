from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class DeductionBase(BaseModel):
    name: str
    type: str
    amount: Decimal = Field(..., decimal_places=2)
    description: Optional[str] = None
    payroll_id: Optional[int] = None


class DeductionCreate(DeductionBase):
    payroll_id: int


class DeductionResponse(DeductionBase):
    deduction_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
