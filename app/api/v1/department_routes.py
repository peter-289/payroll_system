from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.unit_of_work import UnitOfWork
from app.services.department_service import DepartmentService
from typing import List
from app.schemas.department_schema import DepartmentResponse, DepartmentCreate
from app.schemas.position_schema import PositionResponse
from app.domain.exceptions.base import DomainError, DepartmentAlreadyExistsError
from app.db.database_setup import get_db

router = APIRouter(prefix="/api/v1", tags=["Department"])


@router.post("/department", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def add_departments(payload: DepartmentCreate, db: Session = Depends(get_db)):
    try:
        service = DepartmentService(UnitOfWork(db))    
        new_department = service.add_department(payload)
        return new_department
    except DepartmentAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/departments/{department_id}/positions", response_model=List[PositionResponse])
def get_positions_by_department(department_id: int, db: Session = Depends(get_db)):
    try:
        service = DepartmentService(UnitOfWork(db))
        positions = service.get_positions_by_department(department_id)
        return positions
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/departments", response_model=List[DepartmentResponse])
def get_all_departments(db: Session = Depends(get_db)):
    try:
        service = DepartmentService(UnitOfWork(db))
        departments = service.get_all_departments()
        return departments
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/departments/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    try:
        service = DepartmentService(UnitOfWork(db))
        service.delete_department(department_id)
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


