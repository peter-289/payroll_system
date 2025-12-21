from sqlalchemy.orm import Session
from app.models.attendance_model import Attendance
from app.models.employee_model import Employee
from app.schemas.attendance_schema import AttendanceResponse, CheckInOutRequest
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import pytz
from app.db.database_setup import get_db
from datetime import date
from app.exceptions.exceptions import AttendanceServiceError, AttendanceRecordNotFoundError

EAT = pytz.timezone("Africa/Nairobi")


def get_date(target_date: date) -> date:
        if target_date is None:
            target_date = datetime.now(EAT).date()
        return target_date

def validate_date(target_date: date) -> None:
        if target_date > datetime.now(EAT).date():
            raise AttendanceServiceError("Cannot check in for a future date")
        
def check_existing_attendance(db: Session, employee_id: int, target_date: date) -> Attendance:
        existing_attendance = db.query(Attendance).filter(
            Attendance.employee_id == employee_id,
            Attendance.attendance_date == target_date
        ).first()
        if existing_attendance:
            raise AttendanceServiceError("Attendance for this date already recorded")
        return existing_attendance

def create_attendance_record(
    payload: CheckInOutRequest,
    db: Session,
    employee_id: int,
    
) -> Attendance:
        target_date = get_date(payload.attendance_date)
        validate_date(target_date)
        check_existing_attendance(db, employee_id, target_date)
        hours_worked, overtime_hours = calculate_hours_worked(
            payload.check_in, payload.check_out ) if payload.check_in and payload.check_out else (0.0, 0.0)
        now_eat = datetime.now(EAT)
        attendance = Attendance(
            employee_id=employee_id,
            attendance_date=target_date,
            check_in=now_eat,
            status="present",
            hours_worked = hours_worked,
            overtime_hours = overtime_hours,
            remarks=payload.remarks
        )
        db.add(attendance)
        try:
            db.commit()
            db.refresh(attendance)
        except SQLAlchemyError as e:
            db.rollback()
            raise AttendanceServiceError(f"Database error occurred while creating attendance record: {str(e)}")
        return attendance

def calculate_hours_worked(check_in: datetime, check_out: datetime) -> float:
        delta = check_out - check_in
        hours_worked = delta.total_seconds() / 3600.0

        over_time = hours_worked - 8.0 if hours_worked > 8.0 else 0.0
        return round(hours_worked, 2), round(over_time, 2)