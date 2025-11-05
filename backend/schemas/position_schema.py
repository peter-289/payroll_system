from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PositionBase(BaseModel):
    title: str
    department_id: Optional[int] = None
    role_id: Optional[int] = None
    base_salary: Optional[float] = 0.0
    salary_multiplier: Optional[float] = 1.0
    pay_grade: Optional[str] = None
    employment_type: Optional[str] = None


class PositionCreate(PositionBase):
    pass


class PositionUpdate(BaseModel):
    title: Optional[str]
    department_id: Optional[int]
    role_id: Optional[int]
    base_salary: Optional[float]
    salary_multiplier: Optional[float]
    pay_grade: Optional[str]
    employment_type: Optional[str]


class PositionResponse(PositionBase):
    position_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
