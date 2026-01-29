from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class DeductionBase(BaseModel):
    name: str
    is_statutory: bool = Field(default=False)
    is_taxable: bool = Field(default=False)
    has_brackets: bool = Field(default=False)

class DeductionBracket(BaseModel):
    min_amount: Decimal
    max_amount: Optional[Decimal] = None
    rate: Decimal
    fixed_amount: Optional[Decimal] = None

class DeductionCreate(DeductionBase):
    brackets: Optional[List[DeductionBracket]] = []  # List of DeductionBracket

class DeductionResponse(DeductionBase):
    id: int
    code: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class DeductionUpdateBase(BaseModel):
      name: Optional[str]
      is_statutory: bool = Optional[Field(default=False)]
      is_taxable: bool = Optional[Field(default=False)]
      has_brackets: bool = Optional[Field(default=False)]

class DeductionUpdateBracket(BaseModel):
       min_amount: Optional[Decimal]
       max_amount: Optional[Decimal] = None
       rate: Optional[Decimal]
       fixed_amount: Optional[Decimal] = None

class DeductionUpdate(DeductionUpdateBase):
      brackets: Optional[DeductionUpdateBracket]