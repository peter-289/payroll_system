from datetime import date, datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    gender: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    hire_date: date
    employment_status: str
    salary_type: float
    bank_account_number: Optional[str] = None
    bank_name: Optional[str] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[str]
    phone: Optional[str]
    employment_status: Optional[str]
    salary_type: Optional[float]
    department_id: Optional[int]
    position_id: Optional[int]


class EmployeeResponse(EmployeeBase):
    employee_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
