from __future__ import annotations
from pydantic import BaseModel, condecimal, field_validator
from typing import Optional, Annotated, List
from datetime import date, datetime
from app.models.tax_model import TaxType


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


class TaxBase(BaseModel):
    name: str
    description: str
    tax_type: TaxType
    #fixed_amount: Optional[float] = None
    effective_date:datetime
    expiry_date: Optional[datetime] = None
    brackets: Optional[list[TaxBracketCreate]] = []


class TaxCreate(TaxBase):
    pass


class TaxResponse(TaxBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    effective_date: datetime
    expiry_date: Optional[datetime]
    brackets: List[TaxBracketResponse]

    class Config:
         from_attributes = True


class TaxRuleUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    tax_type: Optional[TaxType]
    #fixed_amount: Optional[float]
    effective_date: Optional[datetime]
    expiry_date: Optional[datetime]

    class Config: 
        from_attributes = True

class TaxBracketUpdate(BaseModel):
    min_amount: Optional[float]
    max_amount: Optional[float]
    rate: Optional[float]
    #fixed_amount: Optional[float]

    class Config:
        from_attributes = True