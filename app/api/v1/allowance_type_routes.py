from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database_setup import get_db
from app.schemas.allowance_schema import AllowanceTypeCreate, AllowanceTypeResponse
from app.domain.exceptions.base import AllowanceServiceError, AllowanceTypeNotFoundError
from app.repositories.allowance_repo import AllowanceRepository
from app.services.allowance_service import AllowanceTypeService

router = APIRouter(prefix="/api/v1",tags=["Allowance Types"])

def get_service(db: Session = Depends(get_db))->AllowanceTypeService:
    repo = AllowanceRepository(db)
    return AllowanceTypeService(repo)

#======================================================================================================
#--------------------- CREATE AN ALLOWANCE TYPE -------------------------------------------------------
@router.post("/allowances_types", response_model=AllowanceTypeResponse, status_code=201)
def create_allowance_type(payload: AllowanceTypeCreate, service: AllowanceTypeService = Depends(get_service)):
    try:
        allowance_type = service.create_allowance_type(payload)
        return allowance_type
    except AllowanceServiceError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


#=======================================================================================================
#------------------------ GET ALLOWANCE BY ID ---------------------------------------------------------
@router.get("/allowances_types/{id}", response_model=AllowanceTypeResponse, status_code=200)
def get_allowance_type(id:int, service: AllowanceTypeService = Depends(get_service)):
    try:
        allowance_type = service.get_allowance_type(id)
        return allowance_type
    except AllowanceTypeNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

#=======================================================================================================
#---------------------- GET ALL ALLOWANCES -------------------------------------------------------------
@router.get("/allowances_types", response_model=List[AllowanceTypeResponse])
def get_all_allowances(service: AllowanceTypeService = Depends(get_service)):
    allowance_types = service.get_allowance_types()
    return allowance_types

#======================================================================================================
#------------------------ DELETE ALLOWANCE TYPE -------------------------------------------------------
@router.delete("/allowances_types/{id}", status_code=204)
def delete_allowance_type(allowance_type_id:int, service: AllowanceTypeService = Depends(get_service)):
    try:
        service.delete_allowance_type(allowance_type_id)
        return None
    except AllowanceTypeNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

