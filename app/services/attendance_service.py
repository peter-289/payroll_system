from sqlalchemy.orm import Session
import pytz
from app.models.attendance_model import Attendance
from app.domain.enums import AttendanceStatus
from app.domain.exceptions.base import (
    AttendanceNotApprovedError,AttendanceDomainError, AttendanceServiceError, AttendanceRecordNotFoundError)
from app.domain.rules import attendance_rules
from app.repositories.attendance_repo import AttendanceRepository
from datetime import datetime, date


class AttendanceService:
    """Service to manage employee attendance records."""

    def __init__(self, attendance_repo:AttendanceRepository):
        self.attendance_repo = attendance_repo

    def check_in(
            self, 
            employee_id:int, 
            attendance_date: date | None, 
            check_in_time:datetime, 
            remarks:str | None )-> Attendance:
        try:
            attendance_date = attendance_date or check_in_time.date()

            existing = self.attendance_repo.get_by_employee_and_date(employee_id, attendance_date)
            attendance_rules.validate_check_in_time(check_in_time, attendance_date)
            attendance_rules.ensure_not_duplicate(existing_attendance=existing)

            attendance = Attendance(
                employee_id = employee_id,
                attendance_date = attendance_date,
                check_in = check_in_time,
                remarks = remarks

            )
            return self.attendance_repo.save(attendance)
        except AttendanceDomainError as e:
            raise AttendanceServiceError(message=str(e))
            

    def check_out(
            self,
            employee_id:int,
            attendance_date: date,
            check_out: datetime,
            remarks: str | None)->Attendance:
    
        attendance_date = attendance_date or check_in.date()
        try:
           attendance = self.attendance_repo.get_by_employee_and_date(employee_id, attendance_date)
           attendance_rules.validate_checkout(attendance.check_in, check_out)
           attendance_rules.ensure_can_checkout(attendance)
        
           hours_worked = attendance_rules.calculate_hours(attendance.check_in, check_out)
           attendance_rules.validate_total_working_hours(hours_worked)
           regular, overtime = attendance_rules.split_regular_and_overtime(hours_worked)
           if overtime is not None:
              attendance_rules.validate_overtime_hours(overtime)
           attendance_rules.deny_recheckout(attendance) 
           
           attendance.check_out = check_out
           attendance.regular_hours = regular
           attendance.hours_worked = hours_worked 
           attendance.overtime_hours = overtime
           attendance.remarks = remarks or attendance.remarks

           return self.attendance_repo.update(attendance)
        except AttendanceDomainError as e:
            raise AttendanceServiceError(message=str(e))
        
    def approve_attendance(self, employee_id:int)->Attendance:
        try:
           attendance = self.attendance_repo.get_attendance(employee_id)

           attendance_rules.ensure_can_be_proved(attendance)

           attendance.approved = AttendanceStatus.APPROVED
           self.attendance_repo.update(attendance)
           return attendance
        except AttendanceDomainError as e:
            raise AttendanceServiceError(message=str(e))

    