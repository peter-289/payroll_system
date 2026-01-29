"""Repository for managing Attendance records in the database."""
from sqlalchemy.orm import Session
from datetime import date
from app.models.attendance_model import Attendance
from typing import Optional
from app.domain.enums import AttendanceStatus


class AttendanceRepository:
    """Repository for attendance database operations.
    
    Handles CRUD operations for Attendance records including retrieval by
    employee, date, and status.
    """
    def __init__(self, db: Session):
        """Initialize the attendance repository.
        
        Args:
            db: SQLAlchemy session for database operations.
        """
        self.db = db

    def save_attendance(self, attendance: Attendance) -> Attendance:
        """Save a new attendance record to the database.
        
        Args:
            attendance: Attendance instance to save.
            
        Returns:
            The saved Attendance instance.
        """
        self.db.add(attendance)
        return attendance
    
    def update_attendance(self, attendance: Attendance) -> Attendance:
        """Update an existing attendance record.
        
        Args:
            attendance: Attendance instance with updated values.
            
        Returns:
            The updated Attendance instance.
        """
        self.db.add(attendance)
        return attendance
    
    def get_latest_attendance(self, employee_id: int) -> Optional[Attendance]:
        """Retrieve the latest attendance record for an employee.
        
        Args:
            employee_id: The employee's ID.
            
        Returns:
            Most recent Attendance instance for the employee, or None if not found.
        """
        return (
            self.db.query(Attendance)
            .filter(Attendance.employee_id == employee_id)
            .order_by(Attendance.attendance_date.desc())
            .first()
        )
    
    def get_attendance(self, employee_id: int) -> Optional[Attendance]:
        """Retrieve most recent attendance record for an employee.
        
        Args:
            employee_id: The employee's ID.
            
        Returns:
            Most recent Attendance instance, or None if not found.
        """
        return self.db.query(Attendance)\
            .filter(Attendance.employee_id == employee_id)\
            .order_by(Attendance.attendance_date.desc())\
            .first()
    
    def get_by_employee_and_date(self, employee_id: int, attendance_date: date) -> Optional[Attendance]:
        """Retrieve attendance record for a specific employee and date.
        
        Args:
            employee_id: The employee's ID.
            attendance_date: The date of attendance.
            
        Returns:
            Attendance instance if found for that date, None otherwise.
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
        """Delete an attendance record from the database.
        
        Args:
            attendance: Attendance instance to delete.
        """
        self.db.delete(attendance)

