from fastapi import APIRouter, Depends
from backend.services.insuarance_service import InsuranceService
from backend.schemas.insurance_schema import InsuranceResponse,InsuranceCreate
from sqlalchemy.orm import Session
from backend.database_setups.database_setup import get_db
from typing import List

router = APIRouter(prefix="/api/v1", tags=["Insurance"])

#================================================================================================================
#----------------------------- CREATE INSURANCE -----------------------------------------------------------------
@router.post("/insurances", response_model=InsuranceResponse, status_code=201)
def create_insurance(payload:InsuranceCreate, db:Session = Depends(get_db)):
    service = InsuranceService(db)
    insurance = service.create_insurance(payload)
    return insurance

#===================================================================================================================
#--------------------------- GET INSURANCE -------------------------------------------------------------------------
@router.get("/insurances/{insurance_id}", response_model=InsuranceResponse)
def get_insurance(insurance_id, db:Session = Depends(get_db)):
    service = InsuranceService(db)
    policy = service.get_policy(insurance_id)
    return policy

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
    service = InsuranceService(db)
    service.soft_delete_policy(insurance_id)
    return None

#==================================================================================================================
#--------------------------- DELETE INSURANCE ---------------------------------------------------------------------
@router.delete("/insurances/{insurance_id}", status_code=204)
def delete_insurance(insurance_id:int, db:Session = Depends(get_db)):
    service = InsuranceService(db)
    service.delete_policy(insurance_id)
    return None