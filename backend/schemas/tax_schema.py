from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class TaxBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: Optional[str] = None
    rate: Optional[float] = None
    threshold_min: Optional[float] = None
    fixed_amount: Optional[float] = None
    effective_date: Optional[date] = None
    expiry_date: Optional[date] = None


class TaxCreate(TaxBase):
    pass


class TaxResponse(TaxBase):
    tax_id: int
    created_at: Optional[date]
    updated_at: Optional[date]

    model_config = {"from_attributes": True}
