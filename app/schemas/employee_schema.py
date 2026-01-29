from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from app.models.employee_model import SalaryTypeEnum


class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    gender: str
    date_of_birth: date

    role_name: str
    department_name: str
    position_title: str 
    date_hired: Optional[date] = None
    salary_type: SalaryTypeEnum = SalaryTypeEnum.MONTHLY

    email: str
    phone: str
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

    bank_name: str
    account_number: str
    account_type: Optional[str] = None
      
    model_config = {"from_attributes": True}

class UserResponse(BaseModel):
      id: int
      first_name: str
      username: str
      

      class Config:
          from_attributes = True

class EmployeeResponse(BaseModel):
    id: int
    user: UserResponse
    department_id:int
    position_id:int
    hire_date: date
    approval_status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    salary_type: Optional[SalaryTypeEnum] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    account_type: Optional[str] = None
    
    model_config = {"from_attributes": True}

class EmployeeCreateResponse(BaseModel):
    employee: EmployeeResponse
    temporary_password: str
    message: str = Field(default="Employee created successfully")
    model_config = {"from_attributes": True}
   