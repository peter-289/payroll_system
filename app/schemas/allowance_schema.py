from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.domain.enums import AllowanceCalculationType, AllowancePercentageBasis


class AllowanceTypeBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_taxable: Optional[bool] = True
    is_recurring: Optional[bool] = True
    calculation_type: AllowanceCalculationType
    percentage_of: Optional[AllowancePercentageBasis] = None  # "basic_salary" or "gross_salary"
    default_amount: Optional[Decimal] = Field(default=None, decimal_places=2)
    min_amount: Optional[Decimal] = Field(default=None, decimal_places=2)
    max_amount:Optional[Decimal]


class AllowanceTypeCreate(AllowanceTypeBase):
    pass


class AllowanceTypeResponse(AllowanceTypeBase):
    id: int
    code: str
    status: str
    created_at: Optional[datetime] = None

    
    class Config:
        from_attributes = True


class AllowanceBase(BaseModel):
    payroll_id: int
    allowance_type_id: int
    amount: Decimal = Field(..., decimal_places=2)
    calculation_basis: Optional[str] = None  # e.g., "fixed", "percentage"
    

class AllowanceCreate(AllowanceBase):
    pass


class AllowanceResponse(AllowanceBase):
    id: int
    name: str
    code: str
    status:str
    created_at: Optional[datetime] = None
    
    
    class Config:
        from_attributes = True