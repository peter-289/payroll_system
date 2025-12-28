from typing import Optional, Tuple
from sqlalchemy.orm import Session
from app.models.attendance_model import Attendance
from app.schemas.attendance_schema import CheckInOutRequest
from datetime import datetime, date
from sqlalchemy.exc import SQLAlchemyError
import pytz
from app.exceptions.exceptions import AttendanceServiceError, AttendanceRecordNotFoundError

EAT = pytz.timezone("Africa/Nairobi")


class AttendanceService:
    """Service to manage employee attendance records."""

    def __init__(self, db: Session):
        self.db = db

    def _get_date(self, target_date: Optional[date]) -> date:
        if target_date is None:
            target_date = datetime.now(EAT).date()
        return target_date

    def _validate_date(self, target_date: date) -> None:
        if target_date > datetime.now(EAT).date():
            raise AttendanceServiceError("Cannot check in for a future date")

    def _calculate_hours_worked(self, check_in: datetime, check_out: datetime) -> Tuple[float, float]:
        delta = check_out - check_in
        hours_worked = delta.total_seconds() / 3600.0
        over_time = hours_worked - 8.0 if hours_worked > 8.0 else 0.0
        return round(hours_worked, 2), round(over_time, 2)

    def check_existing_attendance(self, employee_id: int, target_date: date) -> Optional[Attendance]:
        existing_attendance = (
            self.db.query(Attendance)
            .filter(
                Attendance.employee_id == employee_id,
                Attendance.attendance_date == target_date,
            )
            .first()
        )
        if existing_attendance:
            raise AttendanceServiceError("Attendance for this date already recorded")
        return None

    def create_attendance_record(self, payload: CheckInOutRequest, employee_id: int) -> Attendance:
        target_date = self._get_date(getattr(payload, "attendance_date", None))
        self._validate_date(target_date)
        # ensure we don't have a record for the same date
        self.check_existing_attendance(employee_id, target_date)

        hours_worked, overtime_hours = (
            self._calculate_hours_worked(payload.check_in, payload.check_out)
            if payload.check_in and payload.check_out
            else (0.0, 0.0)
        )

        now_eat = datetime.now(EAT)
        attendance = Attendance(
            employee_id=employee_id,
            attendance_date=target_date,
            check_in=now_eat,
            status="present",
            hours_worked=hours_worked,
            overtime_hours=overtime_hours,
            remarks=getattr(payload, "remarks", None),
        )

        self.db.add(attendance)
        try:
            self.db.commit()
            self.db.refresh(attendance)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise AttendanceServiceError(
                f"Database error occurred while creating attendance record: {str(e)}"
            )
        return attendance

    def get_attendance(self, employee_id: int, target_date: Optional[date] = None) -> Attendance:
        target_date = self._get_date(target_date)
        attendance = (
            self.db.query(Attendance)
            .filter(
                Attendance.employee_id == employee_id,
                Attendance.attendance_date == target_date,
            )
            .first()

        )
        if not attendance:
            raise AttendanceRecordNotFoundError(
                f"Attendance for employee {employee_id} on {target_date} not found."
            )
        return attendance

    def get_employee_attendance(self, employee_id:int):
        if employee_id<=0:
            raise AttendanceServiceError("Invalid ID")
        attendance = self.db.query(Attendance).filter(Attendance.employee_id == employee_id).first()
        if not attendance:
            raise AttendanceRecordNotFoundError(f"Attendance with employee id: {employee_id } not found.")
        return attendance