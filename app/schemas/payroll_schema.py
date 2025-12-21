from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import List, Optional


class EarningItem(BaseModel):
    code: str
    amount: float
    taxable: bool = True


class DeductionItem(BaseModel):
    code: str
    amount: float


class AllowanceItem(BaseModel):
    code: str
    amount: float


class PayrollInput(BaseModel):
    employee_id: int
    period_start: date
    period_end: date
    earnings: List[EarningItem]
    deductions: Optional[List[DeductionItem]] = []
    allowances: Optional[List[AllowanceItem]] = []
    config: Optional[dict] = None

    model_config = {"from_attributes": True}


class TaxBreakdownItem(BaseModel):
    name: str
    amount: float
    rate: Optional[float] = None


class LineItem(BaseModel):
    code: str
    description: Optional[str] = None
    amount: float


class PayrollResult(BaseModel):
    employee_id: int
    period_start: date
    period_end: date
    gross_pay: float
    taxable_income: float
    tax_total: float
    tax_breakdown: List[TaxBreakdownItem]
    deductions_total: float
    allowances_total: float
    net_pay: float
    employer_costs: Optional[float] = 0.0
    line_items: Optional[List[LineItem]] = []
    audit: Optional[dict] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"from_attributes": True}
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import date, datetime
from decimal import Decimal


class PayrollBase(BaseModel):
    employee_id: int
    pay_period_start: date
    pay_period_end: date
    basic_salary: Decimal = Field(..., decimal_places=2)
    department_multiplier: Optional[Decimal] = Field(default=Decimal('1.0'), decimal_places=2)
    position_grade_multiplier: Optional[Decimal] = Field(default=Decimal('1.0'), decimal_places=2)
    adjusted_base_salary: Optional[Decimal] = Field(default=Decimal('0.00'), decimal_places=2)
    allowances_breakdown: Optional[Dict[str, Any]] = None
    deductions_breakdown: Optional[Dict[str, Any]] = None
    gross_salary: Optional[Decimal] = Field(default=Decimal('0.00'), decimal_places=2)
    total_deductions: Optional[Decimal] = Field(default=Decimal('0.00'), decimal_places=2)
    total_allowances: Optional[Decimal] = Field(default=Decimal('0.00'), decimal_places=2)
    tax_amount: Optional[Decimal] = Field(default=Decimal('0.00'), decimal_places=2)
    net_salary: Optional[Decimal] = Field(default=Decimal('0.00'), decimal_places=2)
    payment_date: date
    status: str = "draft"
    bank_transaction_id: Optional[str] = None
    version: int = 1
    is_amended: bool = False
    amendment_reason: Optional[str] = None


class PayrollCreate(PayrollBase):
    pass


class PayrollResponse(PayrollBase):
    payroll_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
