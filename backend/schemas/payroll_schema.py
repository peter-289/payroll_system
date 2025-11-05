from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import date, datetime


class PayrollBase(BaseModel):
    employee_id: int
    pay_period_start: date
    pay_period_end: date
    basic_salary: float
    department_multiplier: Optional[float] = 1.0
    position_grade_multiplier: Optional[float] = 1.0
    adjusted_base_salary: Optional[float] = 0.0
    allowances_breakdown: Optional[Dict[str, Any]] = None
    deductions_breakdown: Optional[Dict[str, Any]] = None
    gross_salary: Optional[float] = 0.0
    total_deductions: Optional[float] = 0.0
    net_salary: Optional[float] = 0.0
    payment_date: date
    status: str
    bank_transaction_id: Optional[int] = None


class PayrollCreate(PayrollBase):
    pass


class PayrollResponse(PayrollBase):
    payroll_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
