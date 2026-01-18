from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database_setup import get_db
from app.services.pension_service import PensionService
from app.domain.exceptions.base import PensionServiceError, PensionNotFoundError
from app.schemas.pension_schema import PensionCreate, PensionResponse

router = APIRouter(prefix='/api/v1', tags=['Pension'])


@router.post('/pensions', response_model=PensionResponse, status_code=201)
def create_pension(payload: PensionCreate, db: Session = Depends(get_db)):
    try:
        service = PensionService(db)
        p = service.create_pension(payload)
        return p
    except PensionServiceError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get('/pensions/{pension_id}', response_model=PensionResponse)
def get_pension(pension_id: int, db: Session = Depends(get_db)):
    try:
        service = PensionService(db)
        return service.get_pension(pension_id)
    except PensionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get('/pensions', response_model=list[PensionResponse])
def list_pensions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = PensionService(db)
    return service.list_pensions(skip, limit)


@router.delete('/pensions/{pension_id}', status_code=204)
def delete_pension(pension_id:int, db: Session = Depends(get_db)):
    try:
        service = PensionService(db)
        service.delete_pension(pension_id)
        return None
    except PensionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PensionServiceError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))