from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.unit_of_work import UnitOfWork
from app.schemas.employee_schema import EmployeeCreate, EmployeeResponse, EmployeeCreateResponse, EmployeeUpdate
from app.services.user_service import (
    EmployeeService,
)
from app.db.database_setup import get_db

router = APIRouter(
    prefix="/api/v1", tags=["Employees"],
    #dependencies=[Depends(admin_access)]
)

def get_service(db: Session = Depends(get_db))->EmployeeService:
    """Dependency to get EmployeeService with UnitOfWork."""
    uow = UnitOfWork(db)
    return EmployeeService(uow)

#======================================================================================================
#----------------------------- CREATE EMPLOYEE ------------------------------------------------------
#======================================================================================================
@router.post("/employees", response_model=EmployeeCreateResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, service: EmployeeService = Depends(get_service)):
    result = service.create_employee(employee)
    return result
   

#======================================================================================================
#----------------------------- GET EMPLOYEE BY ID ---------------------------------------------------
#======================================================================================================
@router.get("/employees/{id}", response_model=EmployeeResponse, status_code=status.HTTP_200_OK)
def get_employee_by_id(id: int, service: EmployeeService = Depends(get_service)):
    employee = service.get_employee_by_id(id)
    return employee
    


#======================================================================================================
#----------------------------- GET ALL EMPLOYEES ---------------------------------------------------
#======================================================================================================
@router.get("/employees", response_model=list[EmployeeResponse], status_code=status.HTTP_200_OK)
def get_all_employees(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: Optional[int] = Query(10, ge=1, description="Number of records to return"),
    service: EmployeeService = Depends(get_service)
):
        employees = service.get_all_employees(skip=skip, limit=limit)
        return employees
   


#======================================================================================================
#----------------------------- UPDATE EMPLOYEE ------------------------------------------------------
#======================================================================================================
@router.put("/employees/{id}", response_model=EmployeeResponse, status_code=status.HTTP_200_OK)
def update_employee(id: int, employee_update: EmployeeUpdate, service: EmployeeService = Depends(get_service)):
    if not employee_update.model_dump(exclude_unset=True):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No update data provided")
    updated_employee = service.update_employee(id, employee_update.model_dump(exclude_unset=True))
    return updated_employee
   


#======================================================================================================
#----------------------------- DELETE EMPLOYEE ------------------------------------------------------
#======================================================================================================
@router.delete("/employees/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(id: int, service: EmployeeService = Depends(get_service)):
    service.delete_employee(id)
   