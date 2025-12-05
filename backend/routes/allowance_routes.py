from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database_setups.database_setup import get_db
from backend.models.allowances_model import AllowanceType
from backend.schemas.allowance_schema import AllowanceTypeCreate

router = APIRouter(
    prefix="/allowances",tags=["Allowances"]
)

#======================================================================================================
#--------------------- CREATE AN ALLOWANCE TYPE -----------------------------------------------------
#======================================================================================================
@router.post("/types/", response_model=dict)
def create_allowance_type(
    payload: AllowanceTypeCreate,
    db: Session = Depends(get_db)
):
    # Check if allowance type with same code already exists
    existing_type = db.query(AllowanceType).filter(AllowanceType.code == payload.code).first()
    if existing_type:
        raise HTTPException(status_code=400, detail="Allowance type with this code already exists.")
    
    new_allowance_type = AllowanceType(
        name=payload.name,
        code=payload.code,
        description=payload.description,
        is_taxable=payload.is_taxable,
        is_recurring=payload.is_recurring,
        is_percentage_based=payload.is_percentage_based,
        percentage_of=payload.percentage_of,
        default_amount=payload.default_amount,
        min_amount=payload.min_amount,
        max_amount=payload.max_amount
    )
    
    db.add(new_allowance_type)
    db.commit()
    db.refresh(new_allowance_type)
    
    return {"message": "Allowance type created successfully", "allowance_type_id": new_allowance_type.id}
