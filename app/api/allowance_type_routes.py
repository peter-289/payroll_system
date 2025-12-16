from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database_setup import get_db
from app.services.allowance_type_service import AllowanceTypeService
from app.schemas.allowance_schema import AllowanceTypeCreate, AllowanceTypeResponse

router = APIRouter(prefix="/api/v1",tags=["Allowance Types"])

#======================================================================================================
#--------------------- CREATE AN ALLOWANCE TYPE -------------------------------------------------------
@router.post("/allowances_types", response_model=AllowanceTypeResponse, status_code=201)
def create_allowance_type(payload: AllowanceTypeCreate,db: Session = Depends(get_db)):
    service = AllowanceTypeService(db)
    allowance_type = service.create_allowance(payload)
    return allowance_type


#=======================================================================================================
#------------------------ GET ALLOWANCE BY ID ---------------------------------------------------------
@router.get("/allowances_types/{allowance_type_id}", response_model=AllowanceTypeResponse)
def get_allowance_type(allowance_type_id:int, db:Session = Depends(get_db)):
    service = AllowanceTypeService(db)
    allowance_type = service.get_allowance_type(allowance_type_id)
    return allowance_type

#=======================================================================================================
#---------------------- GET ALL ALLOWANCES -------------------------------------------------------------
@router.get("/allowances_types", response_model=List[AllowanceTypeResponse])
def get_all_allowances(db:Session = Depends(get_db)):
    service = AllowanceTypeService(db)
    allowance_types = service.get_allowance_types()
    return allowance_types

#======================================================================================================
#------------------------ DELETE ALLOWANCE TYPE -------------------------------------------------------
@router.delete("/allowances_types/{allowance_type_id}", status_code=204)
def delete_allowance_type(allowance_type_id:int, db:Session = Depends(get_db)):
    service = AllowanceTypeService(db)
    service.delete_allowance_type(allowance_type_id)
    return None