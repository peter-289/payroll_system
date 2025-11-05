from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AllowanceBase(BaseModel):
    name: str
    type: str
    amount: float
    description: Optional[str] = None
    payroll_id: Optional[int] = None


class AllowanceCreate(AllowanceBase):
    payroll_id: int


class AllowanceResponse(AllowanceBase):
    allowance_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
