from pydantic import BaseModel
from pydantic import BaseModel
from decimal import Decimal
from datetime import date
from typing import List, Optional, Dict
from app.schemas.deduction_schema import DeductionBracket


class ResolvedAllowance(BaseModel):
    allowance_type_id: int
    name: str                      # e.g. "Housing Allowance"
    code: str                      # e.g. "HOUS"
    amount: Decimal                # Final resolved amount for this period
    is_taxable: bool = True

class ResolvedDeductionRule(BaseModel):
    deduction_type_id: int
    name: str                      # e.g. "PAYE"
    code: str                      # e.g. "PAYE"
    is_statutory: bool
    has_brackets: bool
    brackets:  Optional[DeductionBracket] = None # List of bracket dicts if tiered
    rate: Optional[Decimal] = None          # If flat percentage
    fixed_amount: Optional[Decimal] = None

class ResolvedAttendance(BaseModel):
    hours_worked: Decimal = Decimal('0')
    overtime_hours: Decimal = Decimal('0')
    approved: bool = False

class ResolvedLoan(BaseModel):
    monthly_repayment: Decimal = Decimal('0')
    outstanding_balance: Optional[Decimal] = None

class ResolvedInsurance(BaseModel):
    employee_contribution: Decimal = Decimal('0')   # e.g. SHIF

class ResolvedPension(BaseModel):
    employee_contribution: Decimal = Decimal('0')   # NSSF Employee share


class ResolvedPayrollInputs(BaseModel):
    employee_id: int
    period_start: date
    period_end: date
    base_salary: Decimal                   
    allowances: List[ResolvedAllowance] = []
    attendance: ResolvedAttendance
    statutory_deduction_rules: List[ResolvedDeductionRule]
    loan: ResolvedLoan
    insurance: ResolvedInsurance
    pension: ResolvedPension
    position_title: Optional[str] = None
    department_name: Optional[str] = None

    class Config:
        from_attributes = True


# --- Request / Response models for payroll run ---
class PayrollRunRequest(BaseModel):
    employee_id: int
    pay_period_start: date
    pay_period_end: date
    worked_days: Optional[int] = None
    overtime_hours: Optional[Decimal] = None


class PayrollRunResponse(BaseModel):
    id: int
    employee_id: int
    pay_period_start: date
    pay_period_end: date
    payment_date: date
    gross_salary: Decimal
    net_salary: Decimal
    status: str

    class Config:
        orm_mode = True


# --- Backwards-compatible types used by the older PayrollEngine & tests ---
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
    taxable: bool = True


class TaxBreakdownItem(BaseModel):
    name: str
    amount: float
    rate: float


class LineItem(BaseModel):
    code: str
    description: str
    amount: float


class PayrollInput(BaseModel):
    employee_id: int
    period_start: date
    period_end: date
    earnings: List[EarningItem]
    deductions: Optional[List[DeductionItem]] = []
    allowances: Optional[List[AllowanceItem]] = []


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
    employer_costs: float
    line_items: List[LineItem]
    audit: Optional[dict] = None

    class Config:
        orm_mode = True