from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from backend.models.allowances_model import Allowance, AllowanceType
from backend.schemas.allowance_schema import AllowanceCreate, AllowanceTypeCreate
from sqlalchemy.exc import SQLAlchemyError
import random


class AllowanceTypeService:
    def __init__(self, db:Session):
        self.db = db
    
    def _generate_code(self, payload: AllowanceTypeCreate) -> str:
     """Generates a unique code for the allowance type."""
     prefix = payload.name[:4].upper().ljust(4, "X")
     while True:
         suffix = str(random.randint(1000,  9999))
         code = f"{prefix}-{suffix}"
         # check DB for uniqueness
         if not self.db.query(AllowanceType).filter_by(code=code).first():
             break
     return code
     
    

    def create_allowance(self, payload:AllowanceTypeCreate):
        code = self._generate_code(payload)
        existing_type = self.db.query(AllowanceType).filter(AllowanceType.code == code).first()
        if existing_type:
            raise HTTPException(status_code=400, detail="Allowance type with this code already exists!")
        
        new_allowance_type = AllowanceType(
               name=payload.name,
               code=code,
               description=payload.description,
               is_taxable=payload.is_taxable,
               is_recurring=payload.is_recurring,
               is_percentage_based=payload.is_percentage_based,
               percentage_of=payload.percentage_of,
               default_amount=payload.default_amount,
               min_amount=payload.min_amount,
               max_amount=payload.max_amount
            )
        try:
            self.db.add(new_allowance_type)
            self.db.commit()
            self.db.refresh(new_allowance_type)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create new allowance type{e}")
        return new_allowance_type
    
    def get_allowance_types(self):
        allowance_types = self.db.query(AllowanceType).all()
        return allowance_types
    
    def get_allowance_type(self, type_id:int):
        allowance_type = self.db.get(AllowanceType, type_id)
        if not allowance_type:
            raise HTTPException(status_code=404, detail=f"No allowance type with id:{type_id} not found!")
        return allowance_type
    
    def delete_allowance_type(self, type_id:int):
        allowance_type = self.db.get(AllowanceType, type_id)
        if not allowance_type:
            raise HTTPException(status_code=404, detail=f"Allowance type with id {type_id} could not be found!")
        try:
            self.db.delete(allowance_type)
            self.db.commit()
            return {"message":f"Allowance type with id:{type_id} deleted successfuly!"}
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Could not delete allowance type:{e}")