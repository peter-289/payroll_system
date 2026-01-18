from sqlalchemy.orm import Session
from datetime import date
from app.models.attendance_model import Attendance
from typing import Optional
from app.domain.enums import AttendanceStatus


class AttendanceRepository:
    def __init__(self, db:Session):
        """
        Docstring for __init__
        
        :param self: Description
        :param db: Description
        :type db: Session
        """
        self.db = db

    def save(self, attendance: Attendance) -> Attendance:
        """
        Docstring for save
        
        :param self: Description
        :param attendance: Description
        :type attendance: Attendance
        :return: Description
        :rtype: Attendance
        """
        self.db.add(attendance)
        self.db.commit()
        self.db.refresh(attendance)
        return attendance
    
    def update(self, attendance: Attendance) -> Attendance:
        self.db.commit()
        self.db.refresh(attendance)
        return attendance
    
    def get_latest_attendance(self, employee_id:int)-> Attendance:
        return (
            self.db.query(Attendance)
            .filter(Attendance.employee_id == employee_id)
            .order_by(Attendance.attendance_date.desc())
            .first()
        )
    
    def get_attendance(self, employee_id:int)->Optional[Attendance]:
        return self.db.query(Attendance)\
       .filter(Attendance.employee_id==employee_id)\
       .order_by(Attendance.attendance_date.desc())\
       .first()
    

    def get_by_employee_and_date(self, employee_id: int, attendance_date: date) -> Attendance | None:
        return (
            self.db.query(Attendance)
              .filter(
            Attendance.employee_id == employee_id,
            Attendance.attendance_date == attendance_date
        )
        .first()
    )

    
    def delete(self, attendance: Attendance) -> None:
        self.db.delete(attendance)
        self.db.commit()

