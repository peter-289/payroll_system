from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database_setup import get_db
from app.services.department_service import DepartmentService
from typing import List
from app.schemas.department_schema import DepartmentResponse, DepartmentCreate
from app.schemas.position_schema import PositionResponse
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/v1", tags=["Department"])


#=====================================================================================================
#-------------------------- ADD DEPARTMENT -----------------------------------------------------------
@router.post("/department", response_model=DepartmentResponse, status_code=201)
def add_departments(
    payload:DepartmentCreate,
    db:Session = Depends(get_db)
):
    service = DepartmentService(db)    
    new_department = service.add_department(payload)
    return new_department


#======================================================================================================
#----------------------------- GET POSITIONS BY DEPARTMENT --------------------------------------------
@router.get("/departments/{department_id}/positions", response_model=List[PositionResponse])
def get_positions_by_department(
    department_id: int,
    db: Session = Depends(get_db)):
    service = DepartmentService(db)
    positions = service.get_positions_by_department(department_id)
    return positions

#======================================================================================================
#----------------------------- GET ALL DEPARTMENTS ----------------------------------------------------
@router.get("/departments", response_model=List[DepartmentResponse])
def get_all_departments(db: Session = Depends(get_db)):
    service = DepartmentService(db)
    departments = service.get_all_departments()
    return departments

#=====================================================================================================
#---------------------------- DELETE DEPARTMENT BY ID ------------------------------------------------
@router.delete("/departments/{department_id}")
def delete_department(department_id:int, db:Session = Depends(get_db)):
    service = DepartmentService(db)
    service.delete_department(department_id)
    return JSONResponse(
            status_code=200,
            content={"message":f"Department with id:{department_id} removed successfully!"}
        )


