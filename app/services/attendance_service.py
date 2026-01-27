from sqlalchemy.orm import Session
import pytz
from app.models.attendance_model import Attendance
from app.domain.enums import AttendanceStatus
from app.domain.exceptions.base import (
    AttendanceNotApprovedError, AttendanceRecordNotFoundError, DomainError)
from app.domain.rules import attendance_rules
from app.core.unit_of_work import UnitOfWork
from datetime import datetime, date


class AttendanceService:
    """
    Docstring for AttendanceService
    :param self: Description
    :param uow: Description
    :type uow: UnitOfWork
    :return: Description
    :rtype: None
    """
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def check_in(
            self, 
            employee_id:int, 
            attendance_date: date | None, 
            check_in_time:datetime, 
            remarks:str | None )-> Attendance:
        """
        Docstring for check_in
        
        :param self: Refers to the AttendanceService instance
        :param employee_id: An integer representing the unique identifier of the employee
        :type employee_id: int
        :param attendance_date: Date of attendance
        :type attendance_date: date | None
        :param check_in_time: Check in time for the user
        :type check_in_time: datetime
        :param remarks: Remarks left by the user during check-in
        :type remarks: str | None
        :return: Returns an Attendance object representing the recorded attendance
        :rtype: Attendance
        """
        with self.uow:
            attendance_date = attendance_date or check_in_time.date()

            existing = self.uow.attendance_repo.get_by_employee_and_date(employee_id, attendance_date)
            attendance_rules.validate_check_in_time(check_in_time, attendance_date)
            attendance_rules.ensure_not_duplicate(existing_attendance=existing)
            
            # Create new attendance record
            attendance = Attendance(
                employee_id = employee_id,
                attendance_date = attendance_date,
                check_in = check_in_time,
                remarks = remarks

            )
            attendance = self.uow.attendance_repo.save_attendance(attendance)
            self.uow.audit_repo.log_action(
                user_id=employee_id,
                action="check_in",
                metadata=f"Checked in at {check_in_time.isoformat()} on {attendance_date.isoformat()}"
            )
            return attendance
     
            

    def check_out(
            self,
            employee_id:int,
            attendance_date: date,
            check_out: datetime,
            remarks: str | None)->Attendance:
        
        """
        Docstring for check_out
        
        :param self: Refers to the AttendanceService instance
        :param employee_id: An integer representing the unique identifier of the employee
        :type employee_id: int
        :param attendance_date: Date of attendance
        :type attendance_date: date
        :param check_out: Check out time for the user
        :type check_out: datetime
        :param remarks: Remarks left by the user during check-out
        :type remarks: str | None
        :return: Returns an Attendance object representing the updated attendance
        :rtype: Attendance
        """
        attendance_date = attendance_date or check_out.date()
        with self.uow:
           attendance = self.uow.attendance_repo.get_by_employee_and_date(employee_id, attendance_date)
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

           attendance = self.uow.attendance_repo.update_attendance(attendance)
           self.uow.audit_repo.log_action(
                user_id=employee_id,
                action="check_out",
                metadata=f"Checked out at {check_out.isoformat()} on {attendance_date.isoformat()}"
           )
           return attendance
        

    def approve_attendance(self, employee_id:int)->Attendance:
        """
        Docstring for approve_attendance
        
        :param self: Refers to the AttendanceService instance
        :param employee_id: An integer representing the unique identifier of the employee
        :type employee_id: int
        :return: Returns an Attendance object representing the approved attendance
        :rtype: Attendance
        """
        with self.uow:
           attendance = self.uow.attendance_repo.get_attendance(employee_id)
        
           attendance_rules.ensure_can_be_proved(attendance)

           attendance.approved = AttendanceStatus.APPROVED
           self.uow.attendance_repo.update_attendance(attendance)
           self.uow.audit_repo.log_action(
                user_id=employee_id,
                action="approve_attendance",
                metadata=f"Attendance approved for {attendance.attendance_date.isoformat()}"
           )
           return attendance
       
