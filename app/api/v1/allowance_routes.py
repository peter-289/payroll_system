from app.schemas.allowance_schema import AllowanceResponse, AllowanceCreate
from app.services.allowance_service import AllowanceService
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database_setup import get_db
from app.domain.exceptions.base import AllowanceServiceError, AllowanceRecordNotFoundError, AllowanceTypeNotFoundError

router = APIRouter(
    prefix="/api/v1", tags=["Allowances"]
)

#======================================================================================================
#--------------------- CREATE AN ALLOWANCE -------------------------------------------------------
@router.post("/allowances", response_model=AllowanceResponse, status_code=201)
def create_allowance(payload:AllowanceCreate, db:Session=Depends(get_db)):
    try:
        service = AllowanceService(db)
        new_allowance = service.create_allowance(payload)
        return new_allowance
    except AllowanceServiceError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except AllowanceTypeNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

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
    try:
        service = AllowanceService(db)
        allowance = service.get_allowance(allowance_id)
        return allowance
    except AllowanceRecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

#======================================================================================================
#------------------------ DELETE ALLOWANCE -------------------------------------------------------
@router.delete("/allowances/{allowance_id}", status_code=204)
def delete_allowance(allowance_id:int, db:Session=Depends(get_db)):
    try:
        service = AllowanceService(db)
        service.delete_allowance(allowance_id)
        return None
    except AllowanceRecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AllowanceServiceError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))