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
from app.domain.exceptions.base import DomainError
from app.core.unit_of_work import UnitOfWork

#from backend.dependancies.security import get_current_admin
  # your auth dependency

router = APIRouter(prefix="/api/v1", tags=["Attendance"])

# Kenya timezone
EAT = pytz.timezone("Africa/Nairobi")

# Get service
def get_attendance_service(db: Session = Depends(get_db)) -> AttendanceService:
    uow = UnitOfWork(db)
    return AttendanceService(uow)


#===================================================================================================
#--------------------------- CHECK IN OR OUT -------------------------------------------------------
@router.post("/attendance/check-in", response_model=AttendanceResponse, status_code=200)
def check_in(
    payload: CheckInRequest,
    employee: Employee = Depends(get_current_employee),
    service: AttendanceService = Depends(get_attendance_service),
):      
            attendance = service.check_in(
                employee_id=employee["employee_id"],
                attendance_date=payload.attendance_date,
                check_in_time=payload.check_in,
                remarks=payload.remarks
            )
            return attendance


@router.patch("/attendance/check-out", response_model=AttendanceResponse, status_code=status.HTTP_200_OK)
def check_out(
    payload:CheckOutRequest,
    employee = Depends(get_current_employee),
    service: AttendanceService = Depends(get_attendance_service),
):
        
        attendance = service.check_out(  
                employee_id=employee["employee_id"],
                attendance_date=payload.attendance_date,
                check_out=payload.check_out,
                remarks=payload.remarks
            )
        return attendance


    

#=======================================================================================================
#------------------------- APPROVE ATTENDANCE ----------------------------------------------------------
@router.post(
    "/attendance/approve/{id}",
    response_model=AttendanceResponse,
    dependencies=[Depends(admin_access)]
)
def approve_employee_attendance(
    id: int,
    service: AttendanceService = Depends(get_attendance_service),
):
          attendance = service.approve_attendance(id)
          return attendance
    