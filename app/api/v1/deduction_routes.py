from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database_setup import get_db
from app.services.deduction_service import DeductionService
from app.domain.exceptions.base import DomainError, DeductionNotFoundError
from app.schemas.deduction_schema import DeductionCreate, DeductionResponse
from app.repositories.deduction_repo import DeductionRepository

router = APIRouter(prefix='/api/v1', tags=['Deductions'])

def get_service(db: Session = Depends(get_db)) -> DeductionService:
    """Dependency to get DeductionService instance"""
    repo = DeductionRepository(db)
    return DeductionService(repo)


@router.post('/deductions', response_model=DeductionResponse, status_code=201)
def create_deduction(payload: DeductionCreate, service: DeductionService = Depends(get_service)):
    try:
    
        deduction= service.create_deduction_type(payload)
        return deduction
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    
    
@router.get('/deductions/{id}', response_model=DeductionResponse)
def get_deduction(id: int, service: DeductionService = Depends(get_service)):
    try:
        return service.get_deduction(id)
    except DeductionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get('/deductions', response_model=list[DeductionResponse])
def list_deductions(skip: int = 0, limit: int = 100, service: DeductionService = Depends(get_service)):
    return service.list_deductions(skip, limit)


@router.put('/deductions/{id}', response_model=DeductionResponse)
def update_deduction(id:int, payload: DeductionCreate, service: DeductionService = Depends(get_service)):
    try:
        return service.update_deduction(id, payload)
    except DeductionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



@router.delete('/deductions/{deduction_id}', status_code=204)
def delete_deduction(deduction_id:int, db: Session = Depends(get_db)):
    try:
        service = DeductionService(db)
        service.delete_deduction(deduction_id)
        return None
    except DeductionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))