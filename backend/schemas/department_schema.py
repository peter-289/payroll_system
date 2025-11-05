from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    manager_id: Optional[int] = None
    location: Optional[str] = None
    salary_multiplier: Optional[float] = 1.0


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    manager_id: Optional[int]
    location: Optional[str]
    salary_multiplier: Optional[float]


class DepartmentResponse(DepartmentBase):
    department_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
