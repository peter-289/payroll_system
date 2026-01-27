from sqlalchemy.orm import Session
from datetime import date
from app.models.attendance_model import Attendance
from typing import Optional
from app.domain.enums import AttendanceStatus


class AttendanceRepository:
    """Repository for managing Attendance records in the database."""
    def __init__(self, db:Session):
        """
        Docstring for __init__
        
        :param self: Refference to the current class instance
        :param db: A database session
        :type db: Session
        """
        self.db = db


    def save_attendance(self, attendance: Attendance) -> Attendance:
        """
        Docstring for save
        
        :param self: reference to the current instance
        :param attendance: An Attendance object to be saved
        :type attendance: Attendance
        :return: The saved Attendance object
        :rtype: Attendance
        """
        self.db.add(attendance)
        return attendance
    

    def update_attendance(self, attendance: Attendance) -> Attendance:
        """
        Docstring for update_attendance
        
        :param self: Refference to the current class instance
        :param attendance: An attendance object to be updated
        :type attendance: Attendance
        :return: Return the saved attendance object
        :rtype: Attendance
        """
        self.db.add(attendance)
        return attendance
    

    def get_latest_attendance(self, employee_id:int)-> Attendance:
        """
        Docstring for get_latest_attendance
        
        :param self: Refference to the current class instance
        :param employee_id: An integer associated with an employee
        :type employee_id: int
        :return: Returns the latest attendance of an employee
        :rtype: Attendance
        """
        return (
            self.db.query(Attendance)
            .filter(Attendance.employee_id == employee_id)
            .order_by(Attendance.attendance_date.desc())
            .first()
        )
    


    def get_attendance(self, employee_id:int)->Optional[Attendance]:
        """
        Docstring for get_attendance
        
        :param self: Refference to the current class instance
        :param employee_id: An integer associated with an employee
        :type employee_id: int
        :return: Return an attendance for an employee or none
        :rtype: Attendance | None
        """
        return self.db.query(Attendance)\
       .filter(Attendance.employee_id==employee_id)\
       .order_by(Attendance.attendance_date.desc())\
       .first()
    

    def get_by_employee_and_date(self, employee_id: int, attendance_date: date) -> Attendance | None:
        """
        Docstring for get_by_employee_and_date
        
        :param self: Refference to the current class instance
        :param employee_id: An integer associated with an employee
        :type employee_id: int
        :param attendance_date: Attendance date
        :type attendance_date: date
        :return: Return an attendance object by employee and date
        :rtype: Attendance | None
        """
        return (
            self.db.query(Attendance)
              .filter(
            Attendance.employee_id == employee_id,
            Attendance.attendance_date == attendance_date
        )
        .first()
    )

    
    def delete_attendance(self, attendance: Attendance) -> None:
        """
        Docstring for delete
        
        :param self: Refference to the current class instance
        :param attendance: An attendance object to be deleted
        :type attendance: Attendance
        """
        self.db.delete(attendance)

