from app.repositories.allowance_repo import AllowanceRepository
from app.domain.rules import allowance_rules
from app.models.allowances_model import Allowance, AllowanceType, AllowanceStatus
from app.schemas.allowance_schema import AllowanceCreate, AllowanceTypeCreate
from app.domain.exceptions.base import AllowanceServiceError, AllowanceTypeNotFoundError, AllowanceRecordNotFoundError
from sqlalchemy.exc import SQLAlchemyError
import random



class AllowanceService:
    def __init__(self, allowance_repo: AllowanceRepository):
        self.allowance_repo = allowance_repo
         
    def create_allowance(self, payload: AllowanceCreate):
        existing = self.allowance_repo.get_allowance_by_type(payload.allowance_type_id)
        allowance_rules.ensure_no_duplicate_allowance(existing)

        allowance_type = self.allowance_repo.get_allowance_type_by_id(payload.allowance_type_id)
        

        new_allowance = Allowance(
            payroll_id=payload.payroll_id,
            allowance_type_id=payload.allowance_type_id,
            name=allowance_type.name,
            code=allowance_type.code,
            amount=payload.amount,
            is_taxable=allowance_type.is_taxable,
            calculation_basis=payload.calculation_basis,
            
            
        )
        try:
            return self.allowance_repo.save_allowance(new_allowance)
        except SQLAlchemyError as e:
            raise AllowanceServiceError(f"Failed to create new allowance: {e}")
        
    
    def get_allowances(self):
        return self.allowance_repo.get_allowances_by_payroll(None)  # This might need adjustment

    def get_allowance(self, allowance_id: int):
        allowance = self.allowance_repo.get_allowance_by_id(allowance_id)
        if not allowance:
            raise AllowanceRecordNotFoundError(f"Allowance with id {allowance_id} not found!")
        return allowance

    def delete_allowance(self, allowance_id: int):
        allowance = self.allowance_repo.get_allowance_by_id(allowance_id)
        if not allowance:
            raise AllowanceRecordNotFoundError(f"Allowance with id {allowance_id} not found!")
        try:
            self.allowance_repo.delete_allowance(allowance)
            return {"message": f"Allowance with id:{allowance_id} deleted successfully!"}
        except SQLAlchemyError as e:
            raise AllowanceServiceError(f"Could not delete allowance: {e}")


# ============================================================================================
# -------------- ALLOWANCE TYPE METHODS ------------------------------------------------------


class AllowanceTypeService:
    def __init__(self, allowance_repo: AllowanceRepository):
        self.allownce_repo = allowance_repo
    
    
    def _generate_code(self, name: str) -> str:
        prefix = name[:4].upper().ljust(4, "X")
        suffix = str(random.randint(1000,  9999))
        code = f"{prefix}-{suffix}"
        return code

    def create_allowance_type(self, payload:AllowanceTypeCreate):
        code = self._generate_code(payload.name)
        existing_type = self.allownce_repo.get_allowance_type_by_code(code, payload.name)
        allowance_rules.ensure_no_duplicate_allowance(existing_type)
        new_allowance_type = AllowanceType(
               name=payload.name,
               code=code,
               description=payload.description,
               is_taxable=payload.is_taxable,
               calculation_type=payload.calculation_type,
               is_recurring=payload.is_recurring,
               percentage_of=payload.percentage_of,
               default_amount=payload.default_amount,
               min_amount=payload.min_amount,
               max_amount=payload.max_amount
            )
        try:
           self.allownce_repo.save_allowance_type(new_allowance_type)
        except SQLAlchemyError as e:
            self.allownce_repo.roll_back()
            raise AllowanceServiceError(f"Failed to create new allowance type: {e}")
        return new_allowance_type
    

    def get_allowance_types(self):
        allowance_types = self.allownce_repo.get_all_allowance_types()
        return allowance_types
    
    def get_allowance_type(self, id:int):
        allowance_type = self.allownce_repo.get_allowance_type_by_id(id)
        if not allowance_type:
            raise AllowanceTypeNotFoundError(f"Allowance type with id {id} not found!")
        return allowance_type
    
    def delete_allowance_type(self, type_id:int)->None:
        allowance_type = self.allownce_repo.get_allowance_type_by_id(type_id)
        if not allowance_type:
            raise AllowanceTypeNotFoundError(f"Allowance type with id {type_id} not found!")
        try:
           self.allownce_repo.delete_allowance_type(allowance_type)
        except SQLAlchemyError as e:
            self.allownce_repo.roll_back()
            raise AllowanceServiceError(f"Could not delete allowance type: {e}")