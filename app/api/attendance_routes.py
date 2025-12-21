# routers/attendance.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, date, time, timedelta
import pytz
from app.services.attendance_service import (
    create_attendance_record)
from app.db.database_setup import get_db
from app.models.attendance_model import Attendance
from app.models.employee_model import Employee
from app.dependancies.security import get_current_employee
from app.schemas.attendance_schema import AttendanceResponse, CheckInOutRequest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, func
from app.exceptions.exceptions import AttendanceServiceError, AttendanceRecordNotFoundError
#from backend.dependancies.security import get_current_admin
  # your auth dependency

router = APIRouter(prefix="/api/v1", tags=["Attendance"])

# Kenya timezone
EAT = pytz.timezone("Africa/Nairobi")


#===================================================================================================
#--------------------------- CHECK IN OR OUT -------------------------------------------------------
@router.post("/attendance", response_model=AttendanceResponse)
def check_in_or_out(
    payload: CheckInOutRequest = {},
    db: Session = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee)
):
        try:
            create_attendance_record(
                payload,
                db,
                current_employee.id
            )
            
        except AttendanceServiceError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to record attendance due to database error: {str(e)}."
            ) 


#=======================================================================================================
#------------------------- APPROVE ATTENDANCE ----------------------------------------------------------
@router.post(
    "/approve-attendance/{employee_id}",
    response_model=AttendanceResponse,
    summary="HR/Admin approves an employee's attendance record",
    responses={
        200: {"description": "Attendance approved successfully"},
        404: {"description": "Employee or attendance record not found"},
        400: {"description": "Attendance already approved"},
    }
)
def approve_employee_attendance(
    employee_id: int,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin)  # ← Uncomment when you add auth guard
):
    """
    Approve a pending attendance record for a specific employee.
    Only HR/Admins should call this.
    """
    # 1. Fetch employee + their latest (or specific) attendance record in one go
    stmt = (
        select(Attendance)
        .join(Employee, Attendance.employee_id == Employee.id)
        .where(Employee.id == employee_id)
        .order_by(Attendance.attendance_date.desc())  # most recent first
        .limit(1)
    )
    result = db.execute(stmt)
    attendance: Attendance | None = result.scalar_one_or_none()

    # 2. Not found cases
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No attendance record found for employee ID: {employee_id}"
        )

    if attendance.approved == "approved":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Attendance for employee {employee_id} (date: {attendance.attendance_date}) is already approved."
        )

    # 3. Approve it
    try:
        attendance.approved = "approved"           # ← Correct assignment (you had ==)
        attendance.approved_at = func.now()         # ← Optional: track when approved
        attendance.approved_by = "current_user_id" # ← Optional: track who approved (use dependency later)

        db.commit()
        db.refresh(attendance)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to approve attendance due to database error."
        ) from e

    # 4. Success response
    return attendance