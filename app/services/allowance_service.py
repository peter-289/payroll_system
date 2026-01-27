from app.domain.rules import allowance_rules
from app.models.allowances_model import Allowance, AllowanceType
from app.schemas.allowance_schema import AllowanceCreate, AllowanceTypeCreate
from app.domain.exceptions.base import AllowanceTypeNotFoundError, AllowanceRecordNotFoundError
import random
from app.core.unit_of_work import UnitOfWork



class AllowanceService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
         
    def create_allowance(self, payload: AllowanceCreate):
        """
        Docstring for create_allowance
        
        :param self: Description
        :param payload: Description
        :type payload: AllowanceCreate
        """
        # Check if an an allowance exists
        existing = self.uow.allowance_repo.get_allowance_by_type(payload.allowance_type_id)

        # Enforce a business rule to avoid creating duplicate allowances
        allowance_rules.ensure_no_duplicate_allowance(existing)
        
        # Get an allowance type by id from the db
        allowance_type = self.uow.allowance_repo.get_allowance_type_by_id(payload.allowance_type_id)
        
        # Create a new allowance
        new_allowance = Allowance(
            payroll_id=payload.payroll_id,
            allowance_type_id=payload.allowance_type_id,
            name=allowance_type.name,
            code=allowance_type.code,
            amount=payload.amount,
            is_taxable=allowance_type.is_taxable,
            calculation_basis=payload.calculation_basis,
        )
        
        with self.uow:
            return self.uow.allowance_repo.save_allowance(new_allowance)
        
    
    def get_allowances(self):
        return self.uow.allowance_repo.get_allowances_by_payroll(None)  # This might need adjustment

    def get_allowance(self, allowance_id: int):
        allowance = self.uow.allowance_repo.get_allowance_by_id(allowance_id)
        if not allowance:
            raise AllowanceRecordNotFoundError(f"Allowance with id {allowance_id} not found!")
        return allowance

    def delete_allowance(self, allowance_id: int):
        allowance = self.uow.allowance_repo.get_allowance_by_id(allowance_id)
        if not allowance:
            raise AllowanceRecordNotFoundError(f"Allowance with id {allowance_id} not found!")
        with self.uow:
            self.uow.allowance_repo.delete_allowance(allowance)
            

# ============================================================================================
# -------------- ALLOWANCE TYPE METHODS ------------------------------------------------------


class AllowanceTypeService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
    
    
    def _generate_code(self, name: str) -> str:
        prefix = name[:4].upper().ljust(4, "X")
        suffix = str(random.randint(1000,  9999))
        code = f"{prefix}-{suffix}"
        return code

    def create_allowance_type(self, payload:AllowanceTypeCreate):
        code = self._generate_code(payload.name)
        existing_type = self.uow.allowance_repo.get_allowance_type_by_code(code, payload.name)
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
        with self.uow:
               self.uow.allowance_repo.save_allowance_type(new_allowance_type)
        return new_allowance_type
    

    def get_allowance_types(self):
        allowance_types = self.uow.allowance_repo.get_all_allowance_types()
        return allowance_types
    
    def get_allowance_type(self, id:int):
        allowance_type = self.uow.allowance_repo.get_allowance_type_by_id(id)
        if not allowance_type:
            raise AllowanceTypeNotFoundError(f"Allowance type with id {id} not found!")
        return allowance_type
    
    def delete_allowance_type(self, type_id:int)->None:
        allowance_type = self.allownce_repo.get_allowance_type_by_id(type_id)
        if not allowance_type:
            raise AllowanceTypeNotFoundError(f"Allowance type with id {type_id} not found!")
        with self.uow:
           self.allownce_repo.delete_allowance_type(allowance_type)
      