from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    department_id: int
    position_id: Optional[int] = None
    date_of_birth: Optional[date] = None
    date_hired: date
    salary_type: str = "monthly"
    gender: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeResponse(EmployeeBase):
    id: int
    employment_status: str
    approval_status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


   