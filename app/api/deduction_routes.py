from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database_setup import get_db
from app.services.deduction_service import DeductionService
from app.exceptions.exceptions import DeductionServiceError, DeductionNotFoundError
from app.schemas.deduction_schema import DeductionCreate, DeductionResponse

router = APIRouter(prefix='/api/v1', tags=['Deductions'])


@router.post('/deductions', response_model=DeductionResponse, status_code=201)
def create_deduction(payload: DeductionCreate, db: Session = Depends(get_db)):
    try:
        service = DeductionService(db)
        d = service.create_deduction(payload)
        return d
    except DeductionServiceError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get('/deductions/{deduction_id}', response_model=DeductionResponse)
def get_deduction(deduction_id: int, db: Session = Depends(get_db)):
    try:
        service = DeductionService(db)
        return service.get_deduction(deduction_id)
    except DeductionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get('/deductions', response_model=list[DeductionResponse])
def list_deductions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = DeductionService(db)
    return service.list_deductions(skip, limit)


@router.delete('/deductions/{deduction_id}', status_code=204)
def delete_deduction(deduction_id:int, db: Session = Depends(get_db)):
    try:
        service = DeductionService(db)
        service.delete_deduction(deduction_id)
        return None
    except DeductionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DeductionServiceError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))