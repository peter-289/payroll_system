from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database_setup import get_db
from app.services.salary_service import SalaryService
from app.domain.exceptions.base import SalaryServiceError, SalaryNotFoundError
from app.schemas.pension_schema import PensionResponse
from app.models.salary_model import PayFrequency
from datetime import date

router = APIRouter(prefix="/api/v1", tags=["Salary"])


@router.get("/employees/{employee_id}/salary")
def get_employee_salary(employee_id: int, db: Session = Depends(get_db)):
    try:
        service = SalaryService(db)
        salary = service.get_employee_salary(employee_id)
        return salary
    except SalaryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SalaryServiceError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/employees/{employee_id}/salary/effective")
def get_effective_salary(employee_id: int, target_date: date = date.today(), db: Session = Depends(get_db)):
    try:
        service = SalaryService(db)
        salary = service.get_effective_employee_salary(employee_id, target_date)
        return salary
    except SalaryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SalaryServiceError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/employees/{employee_id}/salary", status_code=201)
def add_employee_salary(employee_id: int, amount: float, salary_type: PayFrequency = PayFrequency.MONTHLY, db: Session = Depends(get_db), created_by: int | None = None):
    try:
        service = SalaryService(db)
        salary = service.add_employee_salary(employee_id, amount, salary_type, created_by=created_by)
        return salary
    except SalaryServiceError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/positions/{position_id}/salaries")
def get_position_salaries(position_id: int, db: Session = Depends(get_db)):
    try:
        service = SalaryService(db)
        result = service.get_position_salaries(position_id)
        return result
    except SalaryServiceError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/positions/{position_id}/salaries", status_code=201)
def add_position_salary(position_id: int, amount: float, salary_type: PayFrequency = PayFrequency.MONTHLY, db: Session = Depends(get_db), created_by: int | None = None):
    try:
        service = SalaryService(db)
        ps = service.add_position_salary(position_id, amount, salary_type, created_by=created_by)
        return ps
    except SalaryServiceError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))