from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database_setup import get_db
from app.services.deduction_service import DeductionService
from app.schemas.deduction_schema import DeductionCreate, DeductionResponse, DeductionUpdate
from app.core.unit_of_work import UnitOfWork
from app.core.security import admin_access

router = APIRouter(
    prefix='/api/v1',
    tags=['Deductions'],
    dependencies=[Depends(admin_access)]
    )

def get_service(session: Session = Depends(get_db)) -> DeductionService:
    """Dependency to get DeductionService instance"""
    uow = UnitOfWork(session)
    return DeductionService(uow)


@router.post('/deductions', response_model=DeductionResponse, status_code=201)
def create_deduction(payload: DeductionCreate, service: DeductionService = Depends(get_service)):
        deduction= service.create_deduction_type(payload)
        return deduction
    
    
@router.get('/deductions/{id}', response_model=DeductionResponse)
def get_deduction(id: int, service: DeductionService = Depends(get_service)):
        return service.get_deduction(id)
    

@router.get('/deductions', response_model=list[DeductionResponse])
def list_deductions(skip: int = 0, limit: int = 100, service: DeductionService = Depends(get_service)):
    return service.list_deductions(skip, limit)


@router.put('/deductions/{id}', response_model=DeductionResponse)
def update_deduction(id:int, payload: DeductionUpdate, service: DeductionService = Depends(get_service)):
        return service.update_deduction(id, payload)
    


@router.delete('/deductions/{id}', status_code=204)
def delete_deduction(id:int, service: DeductionService = Depends(get_service)):
        service.delete_deduction(id)
        
   