from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.database_setup import get_db
from app.schemas.employee_schema import EmployeeCreate, EmployeeResponse, EmployeeCreateResponse, EmployeeUpdate
from app.services.user_service import (
    EmployeeService,
)
from app.domain.exceptions.base import (
    EmployeeServiceError,
    UserAlreadyExistsError,
    RoleNotFoundError,
    DepartmentNotFoundError,
    PositionNotFoundError,
    ContactAlreadyExistsError,
    BankAccountAlreadyExistsError,
    EmployeeNotFoundError,
)


router = APIRouter(
    prefix="/api/v1", tags=["Employees"],
    #dependencies=[Depends(admin_access)]
)


#======================================================================================================
#----------------------------- CREATE EMPLOYEE ------------------------------------------------------
#======================================================================================================
@router.post("/employees", response_model=EmployeeCreateResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    try:
        employee_service = EmployeeService(db)
        result = employee_service.create_employee(employee)
        return result
    except UserAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    except (RoleNotFoundError, DepartmentNotFoundError, PositionNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid role, department, or position: {str(e)}")
    except (ContactAlreadyExistsError, BankAccountAlreadyExistsError) as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Contact or bank account already exists: {str(e)}")
    except EmployeeServiceError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{str(e)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Server Error: {str(e)}")
#======================================================================================================
#----------------------------- GET EMPLOYEE BY ID ---------------------------------------------------
#======================================================================================================
@router.get("/employees/{employee_id}", response_model=EmployeeResponse, status_code=status.HTTP_200_OK)
def get_employee_by_id(employee_id: int, db: Session = Depends(get_db)):
    if employee_id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employee ID must be positive")
    try:
        employee_service = EmployeeService(db)
        employee = employee_service.get_employee_by_id(employee_id)
        return employee
    except EmployeeNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    except EmployeeServiceError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve employee")

#======================================================================================================
#----------------------------- GET ALL EMPLOYEES ---------------------------------------------------
#======================================================================================================
@router.get("/employees", response_model=list[EmployeeResponse], status_code=status.HTTP_200_OK)
def get_all_employees(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: Optional[int] = Query(10, ge=1, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    try:
        employee_service = EmployeeService(db)
        employees = employee_service.get_all_employees(skip=skip, limit=limit)
        return employees
    except EmployeeServiceError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve employees")

#======================================================================================================
#----------------------------- UPDATE EMPLOYEE ------------------------------------------------------
#======================================================================================================
@router.put("/employees/{employee_id}", response_model=EmployeeResponse, status_code=status.HTTP_200_OK)
def update_employee(employee_id: int, employee_update: EmployeeUpdate, db: Session = Depends(get_db)):
    if employee_id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employee ID must be positive")
    if not employee_update.model_dump(exclude_unset=True):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No update data provided")
    try:
        employee_service = EmployeeService(db)
        updated_employee = employee_service.update_employee(employee_id, employee_update.model_dump(exclude_unset=True))
        return updated_employee
    except EmployeeNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    except (RoleNotFoundError, DepartmentNotFoundError, PositionNotFoundError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role, department, or position")
    except EmployeeServiceError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update employee")

#======================================================================================================
#----------------------------- DELETE EMPLOYEE ------------------------------------------------------
#======================================================================================================
@router.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    if employee_id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employee ID must be positive")
    try:
        employee_service = EmployeeService(db)
        employee_service.delete_employee(employee_id)
    except EmployeeNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    except EmployeeServiceError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete employee")
