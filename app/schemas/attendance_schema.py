from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from app.domain.enums import AttendanceStatus

class CheckInRequest(BaseModel):
    attendance_date: Optional[date] = Field(default=None)
    check_in: datetime
    remarks: Optional[str] = Field(default=None)

class CheckOutRequest(BaseModel):
    attendance_date: Optional[date] =  Field(default=None)
    check_out: datetime
    remarks: Optional[str] = Field(default=None)

class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    attendance_date: date
    check_in: Optional[datetime]
    check_out: Optional[datetime]
    hours_worked: float
    overtime_hours: float
    remarks: Optional[str]
    approved: Optional[AttendanceStatus]

    class Config:
        from_attributes = True