from fastapi import APIRouter, Depends, HTTPException, status
from app.services.insurance_service import InsuranceService
from app.schemas.insurance_schema import InsuranceResponse,InsuranceCreate
from sqlalchemy.orm import Session
from app.db.database_setup import get_db
from typing import List
from app.domain.exceptions.base import DomainError, InsuranceRecordNotFoundError

router = APIRouter(prefix="/api/v1", tags=["Insurance"])

#================================================================================================================
#----------------------------- CREATE INSURANCE -----------------------------------------------------------------
@router.post("/insurances", response_model=InsuranceResponse, status_code=201)
def create_insurance(payload:InsuranceCreate, db:Session = Depends(get_db)):
    try:
        service = InsuranceService(db)
        insurance = service.create_insurance(payload)
        return insurance
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

#===================================================================================================================
#--------------------------- GET INSURANCE -------------------------------------------------------------------------
@router.get("/insurances/{insurance_id}", response_model=InsuranceResponse)
def get_insurance(insurance_id, db:Session = Depends(get_db)):
    try:
        service = InsuranceService(db)
        policy = service.get_policy(insurance_id)
        return policy
    except InsuranceRecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

#====================================================================================================================
#--------------------------- GET ALL INSURANCES ---------------------------------------------------------------------
@router.get("/insurances", response_model=List[InsuranceResponse])
def get_all_insurances(db:Session = Depends(get_db)):
    service = InsuranceService(db)
    return service.get_all_policies()

#====================================================================================================================
#--------------------------- SOFT DELETE INSURANCE ------------------------------------------------------------------
@router.delete("/insurances/{insurance_id}", status_code=204)
def soft_delete_policy(insurance_id:int, db:Session = Depends(get_db)):
    try:
        service = InsuranceService(db)
        service.soft_delete_policy(insurance_id)
        return None
    except InsuranceRecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

#==================================================================================================================
#--------------------------- DELETE INSURANCE ---------------------------------------------------------------------
@router.delete("/insurances/{insurance_id}", status_code=204)
def delete_insurance(insurance_id:int, db:Session = Depends(get_db)):
    try:
        service = InsuranceService(db)
        service.delete_policy(insurance_id)
        return None
    except InsuranceRecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))