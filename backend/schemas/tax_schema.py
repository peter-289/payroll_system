from __future__ import annotations
from pydantic import BaseModel, condecimal, field_validator
from typing import Optional, Annotated, List
from datetime import date, datetime
from backend.models.tax_model import TaxType


Money = Annotated[float, condecimal(max_digits=10, decimal_places=2)]
Rate = Annotated[float, condecimal(max_digits=5, decimal_places=2)]


class TaxBracketCreate(BaseModel):
    min_amount: Money
    max_amount: Optional[Money] = None
    rate: Rate


class TaxBracketResponse(BaseModel):
    id: int
    min_amount: float
    max_amount: Optional[float]
    rate: float

    class Config:
         from_attributes = True




@field_validator("max_amount")
def check_bounds(cls, v, values):
        if v is not None and "min_amount" in values and v < values["min_amount"]:
            raise ValueError("max_amount must be >= min_amount")
        return v


class TaxBase(BaseModel):
    name: str
    description: str
    type: TaxType
    #fixed_amount: Optional[float] = None
    effective_date:date
    expiry_date: Optional[date] = None
    brackets: Optional[list[TaxBracketCreate]] = []


class TaxCreate(TaxBase):
    pass


class TaxResponse(TaxBase):
    id: int
    created_at: Optional[date]
    updated_at: Optional[date]
    effective_date: datetime
    expiry_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    brackets: List[TaxBracketResponse]

    class Config:
         from_attributes = True


class TaxRuleUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    type: Optional[TaxType]
    #fixed_amount: Optional[float]
    effective_date: Optional[date]
    expiry_date: Optional[date]

    class Config:
        from_attributes = True

class TaxBracketUpdate(BaseModel):
    min_amount: Optional[float]
    max_amount: Optional[float]
    rate: Optional[float]
    #fixed_amount: Optional[float]

    class Config:
        from_attributes = True