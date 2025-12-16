from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

class CheckInOutRequest(BaseModel):
    attendance_date: Optional[date] = Field(default=None)  # Allow manual date (admin only later)
    remarks: Optional[str] = Field(default=None)

class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    attendance_date: date
    check_in: Optional[datetime]
    check_out: Optional[datetime]
    status: str
    hours_worked: float
    overtime_hours: float
    remarks: Optional[str]

    class Config:
        from_attributes = True