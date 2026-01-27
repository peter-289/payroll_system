from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database_setup import get_db
from app.services.loan_service import LoanService
from app.domain.exceptions.base import DomainError, LoanNotFoundError
from app.schemas.loan_schema import LoanCreate, LoanResponse

router = APIRouter(prefix='/api/v1', tags=['Loans'])


@router.post('/loans', response_model=LoanResponse, status_code=201)
def create_loan(payload: LoanCreate, db: Session = Depends(get_db)):
    try:
        service = LoanService(db)
        l = service.create_loan(payload)
        return l
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get('/loans/{loan_id}', response_model=LoanResponse)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    try:
        service = LoanService(db)
        return service.get_loan(loan_id)
    except LoanNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get('/loans', response_model=list[LoanResponse])
def list_loans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = LoanService(db)
    return service.list_loans(skip, limit)


@router.delete('/loans/{loan_id}', status_code=204)
def delete_loan(loan_id:int, db: Session = Depends(get_db)):
    try:
        service = LoanService(db)
        service.delete_loan(loan_id)
        return None
    except LoanNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))