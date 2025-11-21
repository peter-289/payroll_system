# routers/attendance.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, date, time, timedelta
import pytz
from backend.database_setups.database_setup import get_db
from backend.models.attendance_model import Attendance
from backend.models.employee_model import Employee
from backend.dependancies.security import get_current_employee
from backend.schemas.attendance_schema import AttendanceResponse, CheckInOutRequest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, func
#from backend.dependancies.security import get_current_admin
  # your auth dependency

router = APIRouter(prefix="/attendance", tags=["Attendance"])

# Kenya timezone
EAT = pytz.timezone("Africa/Nairobi")


#===================================================================================================
#--------------------------- CHECK IN OR OUT -------------------------------------------------------
@router.post("/check-in-out", response_model=AttendanceResponse)
def check_in_or_out(
    payload: CheckInOutRequest = {},
    db: Session = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee)
):
    # 1. Use provided date or today (in EAT)
    target_date = payload.attendance_date
    if target_date is None:
        target_date = datetime.now(EAT).date()

    # Block future dates (unless admin — you can add role check later)
    if target_date > datetime.now(EAT).date():
        raise HTTPException(
            status_code=400,
            detail="Cannot check in for a future date"
        )

    # 2. Find or create attendance record for this employee + date
    attendance = db.query(Attendance).filter(
        Attendance.employee_id == current_employee["employee_id"],
        Attendance.attendance_date == target_date
    ).first()

    now_eat = datetime.now(EAT)

    if not attendance:
        # First time today → CHECK-IN
        attendance = Attendance(
            employee_id=current_employee["employee_id"],
            attendance_date=target_date,
            check_in=now_eat,
            status="present",
            remarks=payload.remarks
        )
        db.add(attendance)
        db.commit()
        db.refresh(attendance)
        return attendance

    # Already has record → CHECK-OUT (or update check-in if missing)
    if attendance.check_in is None:
        # Rare case: record exists but no check-in → allow check-in
        attendance.check_in = now_eat
        attendance.remarks = payload.remarks or attendance.remarks

    if attendance.check_out is None:
        # Now doing check-out
        attendance.check_out = now_eat
        attendance.remarks = payload.remarks or attendance.remarks

        # Calculate hours
        if attendance.check_in:
            delta = attendance.check_out - attendance.check_in
            total_hours = delta.total_seconds() / 3600

            # Standard 8-hour workday (Kenya Labour Law)
            regular_hours = min(total_hours, 8.0)
            overtime = max(0.0, total_hours - 8.0)

            attendance.hours_worked = round(regular_hours, 2)
            attendance.overtime_hours = round(overtime, 2)

            # Optional: mark late arrival
            if attendance.check_in.time() > time(9, 0):  # after 9 AM
                attendance.status = "late"

    else:
        # Already checked out → maybe allow update (admin only later)
        raise HTTPException(
            status_code=400,
            detail="Already checked out for today"
        )

    db.commit()
    db.refresh(attendance)
    return attendance


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