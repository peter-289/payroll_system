from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LoanBase(BaseModel):
    employee_id: Optional[int]
    type: Optional[str]
    principle_amount: Optional[float]
    balance_amount: Optional[float]
    installment_amount: Optional[float]
    interest_rate: Optional[float]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    status: Optional[str]
    description: Optional[str]


class LoanCreate(LoanBase):
    pass


class LoanResponse(LoanBase):
    loan_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}
