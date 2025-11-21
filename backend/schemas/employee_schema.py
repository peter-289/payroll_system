from pydantic import BaseModel, EmailStr, computed_field
from datetime import date
from typing import Optional

class EmployeeCreateSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    role_name: str
    date_of_birth: str
    department_name: str
    position_title: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    account_type: Optional[str] = None


class EmployeeResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    employment_status: str  
    salary_type: str
    #department_name: Optional[str] = None
    #position_title: Optional[str] = None

    class Config:
        from_attributes = True


   