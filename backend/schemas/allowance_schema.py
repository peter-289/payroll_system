from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class AllowanceTypeBase(BaseModel):
    name: str
    code: str
    is_taxable: Optional[bool] = True
    is_percentage_based: Optional[bool] = False
    default_amount: Optional[Decimal] = Field(default=None, decimal_places=2)
    min_amount: Optional[Decimal] = Field(default=None, decimal_places=2)
    max_amount: Optional[Decimal] = Field(default=None, decimal_places=2)
    percentage_of: Optional[str] = None  # "basic_salary" or "gross_salary"
    is_recurring: Optional[bool] = True


class AllowanceTypeCreate(AllowanceTypeBase):
    pass


class AllowanceTypeResponse(AllowanceTypeBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AllowanceBase(BaseModel):
    payroll_id: int
    name: str
    amount: Decimal = Field(..., decimal_places=2)
    is_taxable: Optional[bool] = True


class AllowanceCreate(AllowanceBase):
    pass


class AllowanceResponse(AllowanceBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True