from backend.schemas.allowance_schema import AllowanceResponse, AllowanceCreate
from backend.services.allowance_service import AllowanceService
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database_setups.database_setup import get_db

router = APIRouter(
    prefix="/api/v1", tags=["Allowances"]
)

#======================================================================================================
#--------------------- CREATE AN ALLOWANCE -------------------------------------------------------
@router.post("/allowances", response_model=AllowanceResponse, status_code=201)
def create_allowance(payload:AllowanceCreate, db:Session=Depends(get_db)):
    service = AllowanceService(db)
    new_allowance = service.create_allowance(payload)
    return new_allowance

#=======================================================================================================
#---------------------- GET ALL ALLOWANCES -------------------------------------------------------------
@router.get("/allowances", response_model=list[AllowanceResponse])
def get_allowances(db:Session=Depends(get_db)):
    service = AllowanceService(db)
    allowances = service.get_allowances()
    return allowances

#=======================================================================================================
#------------------------ GET ALLOWANCE BY ID ---------------------------------------------------------
@router.get("/allowances/{allowance_id}", response_model=AllowanceResponse)
def get_allowance(allowance_id:int, db:Session=Depends(get_db)):
    service = AllowanceService(db)
    allowance = service.get_allowance(allowance_id)
    return allowance

#======================================================================================================
#------------------------ DELETE ALLOWANCE -------------------------------------------------------
@router.delete("/allowances/{allowance_id}", status_code=204)
def delete_allowance(allowance_id:int, db:Session=Depends(get_db)):
    service = AllowanceService(db)
    service.delete_allowance(allowance_id)
    return None