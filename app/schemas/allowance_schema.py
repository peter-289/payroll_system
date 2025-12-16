from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class AllowanceTypeBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_taxable: Optional[bool] = True
    is_recurring: Optional[bool] = True
    is_percentage_based: Optional[bool] = False
    percentage_of: Optional[str] = None  # "basic_salary" or "gross_salary"
    default_amount: Optional[Decimal] = Field(default=None, decimal_places=2)
    min_amount: Optional[Decimal] = Field(default=None, decimal_places=2)
    max_amount:Optional[Decimal]


class AllowanceTypeCreate(AllowanceTypeBase):
    pass


class AllowanceTypeResponse(AllowanceTypeBase):
    id: int
    code: str
    is_active: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AllowanceBase(BaseModel):
    payroll_id: int
    allowance_type_id: int
    amount: Decimal = Field(..., decimal_places=2)
    description: Optional[str] = None
    calculation_basis: Optional[str] = None  # e.g., "fixed", "percentage"
    Reference_number: Optional[str] = None

class AllowanceCreate(AllowanceBase):
    pass


class AllowanceResponse(AllowanceBase):
    id: int
    name: str
    code: str
    status:str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True