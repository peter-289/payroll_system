# routers/attendance.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import pytz
from app.services.attendance_service import AttendanceService
from app.db.database_setup import get_db
from app.models.attendance_model import Attendance
from app.models.employee_model import Employee
from app.core.security import get_current_employee, admin_access, hr_access
from app.schemas.attendance_schema import AttendanceResponse, CheckInRequest, CheckOutRequest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, func
from app.domain.exceptions.base import AttendanceServiceError
from app.repositories.attendance_repo import AttendanceRepository

#from backend.dependancies.security import get_current_admin
  # your auth dependency

router = APIRouter(prefix="/api/v1", tags=["Attendance"])

# Kenya timezone
EAT = pytz.timezone("Africa/Nairobi")


#===================================================================================================
#--------------------------- CHECK IN OR OUT -------------------------------------------------------
@router.post("/attendance/check-in", response_model=AttendanceResponse, status_code=200)
def check_in(
    payload: CheckInRequest,
    employee: Employee = Depends(get_current_employee),
    db:Session = Depends(get_db)
):      
        attendance_repo = AttendanceRepository(db)
        attendance_service = AttendanceService(attendance_repo)
        try:
            attendance = attendance_service.check_in(
                
                employee_id=employee["employee_id"],
                attendance_date=payload.attendance_date,
                check_in_time=payload.check_in,
                remarks=payload.remarks
            )
            return attendance

        except AttendanceServiceError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except SQLAlchemyError  as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to record attendance due to database error: {str(e)}."
            ) 

@router.patch("/attendance/check-out", response_model=AttendanceResponse, status_code=status.HTTP_200_OK)
def check_out(
    payload:CheckOutRequest,
    employee = Depends(get_current_employee),
    db:Session = Depends(get_db),
):
        attendance_repo = AttendanceRepository(db)
        attendance_service = AttendanceService(attendance_repo)
        try:
            attendance = attendance_service.check_out(
                
                employee_id=employee["employee_id"],
                attendance_date=payload.attendance_date,
                check_out=payload.check_out,
                remarks=payload.remarks
            )
            return attendance

        except AttendanceServiceError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except SQLAlchemyError  as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to record attendance due to database error: {str(e)}."
            ) 

    

#=======================================================================================================
#------------------------- APPROVE ATTENDANCE ----------------------------------------------------------
@router.post(
    "/attendance/approve/{employee_id}",
    response_model=AttendanceResponse,
    dependencies=[Depends(admin_access)]
)
def approve_employee_attendance(
    employee_id: int,
    db: Session = Depends(get_db),

):
     repo = AttendanceRepository(db)
     service = AttendanceService(repo)

     try:
          attendance = service.approve_attendance(employee_id)
          return attendance
     except AttendanceServiceError as e:
          raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST,
               detail=f"Error:{e}"
          )
     except SQLAlchemyError as e:
          raise HTTPException(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail=f"Database error: {e}"
          )