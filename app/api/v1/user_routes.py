"""Employee management API routes."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.unit_of_work import UnitOfWork
from app.schemas.employee_schema import EmployeeCreate, EmployeeResponse, EmployeeCreateResponse, EmployeeUpdate
from app.services.user_service import (
    EmployeeService,
)
from app.core.security import admin_access
from app.db.database_setup import get_db

router = APIRouter(
    prefix="/api/v1", tags=["Employees"],
    dependencies=[Depends(admin_access)]
)

def get_service(db: Session = Depends(get_db)) -> EmployeeService:
    """Dependency to get EmployeeService with UnitOfWork.
    
    Args:
        db: Database session.
        
    Returns:
        EmployeeService instance.
    """
    uow = UnitOfWork(db)
    return EmployeeService(uow)

#======================================================================================================
#----------------------------- CREATE EMPLOYEE ------------------------------------------------------
#======================================================================================================
@router.post("/employees", response_model=EmployeeCreateResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, service: EmployeeService = Depends(get_service)):
    """Create a new employee record.
    
    Args:
        employee: Employee creation data.
        service: EmployeeService instance.
        
    Returns:
        EmployeeCreateResponse with created employee details including temporary password.
    """
    result = service.create_employee(employee)
    return result

#======================================================================================================
#----------------------------- GET EMPLOYEE BY ID ---------------------------------------------------
#======================================================================================================
@router.get("/employees/{id}", response_model=EmployeeResponse, status_code=status.HTTP_200_OK)
def get_employee_by_id(id: int, service: EmployeeService = Depends(get_service)):
    """Retrieve a specific employee by ID.
    
    Args:
        id: Employee ID.
        service: EmployeeService instance.
        
    Returns:
        EmployeeResponse with employee details.
    """
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
    """Retrieve all employees with pagination.
    
    Args:
        skip: Number of records to skip for pagination.
        limit: Maximum number of records to return.
        service: EmployeeService instance.
        
    Returns:
        List of EmployeeResponse objects.
    """
    employees = service.get_all_employees(skip=skip, limit=limit)
    return employees

#======================================================================================================
#----------------------------- UPDATE EMPLOYEE ------------------------------------------------------
#======================================================================================================
@router.put("/employees/{id}", response_model=EmployeeResponse, status_code=status.HTTP_200_OK)
def update_employee(id: int, employee_update: EmployeeUpdate, service: EmployeeService = Depends(get_service)):
    """Update an existing employee record.
    
    Args:
        id: Employee ID to update.
        employee_update: Partial employee data to update.
        service: EmployeeService instance.
        
    Returns:
        EmployeeResponse with updated employee details.
        
    Raises:
        HTTPException: 400 if no update data provided.
    """
    if not employee_update.model_dump(exclude_unset=True):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No update data provided")
    updated_employee = service.update_employee(id, employee_update.model_dump(exclude_unset=True))
    return updated_employee

#======================================================================================================
#----------------------------- DELETE EMPLOYEE ------------------------------------------------------
#======================================================================================================
@router.delete("/employees/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(id: int, service: EmployeeService = Depends(get_service)):
    """Delete an employee record.
    
    Args:
        id: Employee ID to delete.
        service: EmployeeService instance.
    """
    service.delete_employee(id)
   