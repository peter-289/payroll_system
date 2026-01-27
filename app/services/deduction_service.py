from os import name
from app.models.deductions_model import Deduction, DeductionType, DeductionBracket
from app.repositories.deduction_repo import DeductionRepository
from app.domain.rules import deduction_rules
from app.domain.exceptions.base import DomainError, DeductionNotFoundError
from sqlalchemy.exc import SQLAlchemyError
from app.utils.tax_bracket_validator import validate_no_overlaps
import uuid
from app.core.unit_of_work import UnitOfWork


class DeductionService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
    
    def _generate_deduction_code(self, name: str) -> str:
        prefix = name[:3].upper()
        unique_suffix = uuid.uuid4().hex[:6].upper()
        code = f"{prefix}-{unique_suffix}"
        return code
    
    def create_deduction_brackets(self, type_id: int, brackets: list)-> None:
        """
        Docstring for create_deduction_brackets
        
        :param self: Description
        :param type_id: Description
        :type type_id: int
        :param brackets: Description
        :type brackets: list
        """
        if type_id <= 0:
            raise DomainError("Invalid ID")
        deduction_rules.validate_bracket(brackets)
        for bracket in brackets:
            db_bracket = DeductionBracket(
                deduction_type_id=type_id,
                min_amount=bracket.min_amount,
                max_amount=bracket.max_amount,
                rate=bracket.rate,
                fixed_amount=bracket.fixed_amount
            )
            self.uow.deduction_repo.save_deduction_bracket(db_bracket)
            

    def create_deduction_type(self, payload):
        """
        Docstring for create_deduction_type
        
        :param self: Description
        :param payload: Description
        """

        code = self._generate_deduction_code(payload.name)
        existing = self.deduction_repo.get_deduction_by_name(payload.name)
        deduction_rules.check_unique_names(payload.name, existing.name if existing else "")

        deduction = DeductionType(
            name=payload.name,
            code=code,
            is_statutory=payload.is_statutory,
            is_taxable=payload.is_taxable,
            has_brackets=payload.has_brackets
        )
        try:
            saved_deduction = self.deduction_repo.save_deduction_type(deduction)
            if payload.has_brackets:
                if not payload.brackets:
                    raise DomainError("Brackets must be provided for deductions with brackets")
                self.create_deduction_brackets(saved_deduction.id, payload.brackets)
            
            return saved_deduction
        except SQLAlchemyError as e:
            raise DomainError(f"Failed to create deduction: {e}")


    def get_taxable_deduction(self, id: int)-> DeductionType:
        if id <= 0:
            raise DomainError("Invalid ID")
        deduction_type = self.deduction_repo.get_taxable_deduction_type(id)
        if not deduction_type:
            raise DeductionNotFoundError(f"Deduction with id {id} not found")
        return deduction_type


    def list_deductions(self, skip: int = 0, limit: int = 100):
        all_deductions = self.deduction_repo.get_all_deduction_types()
        return all_deductions[skip:skip + limit]

    def update_deduction(self, deduction_id: int, payload):
        if deduction_id <= 0:
            raise DomainError("Invalid ID")
        d = self.deduction_repo.get_deduction_type_by_id(deduction_id)
        if not d:
            raise DeductionNotFoundError(f"Deduction with id {deduction_id} not found")

        # Prevent duplicate names
        if payload.name and payload.name != d.name:
            existing = self.deduction_repo.get_deduction_type_by_code(payload.code)
            #dedction_rules.ensure_no_duplicate_deduction_type(existing, payload.name)

        try:
            d.name = payload.name
            d.is_statutory = payload.is_statutory
            d.is_taxable = payload.is_taxable
            d.has_brackets = payload.has_brackets

            
            if d.has_brackets and getattr(payload, 'brackets', None):
                validate_no_overlaps(payload.brackets)
                with self.uow:
                    deduction_type = self.uow.deduction_repo.get_deduction_type_by_id(d.id)
                    self.uow.deduction_repo.delete_deduction_type(deduction_type)
                    self.create_deduction_brackets(d.id, payload.brackets)
            elif not d.has_brackets:
                self.uow.deduction_repo.delete_deduction_type(deduction_type)  
              
            return self.uow.deduction_repo.update_deduction_type(d)
        except SQLAlchemyError as e:
            raise DomainError(f"Failed to update deduction: {e}")


    def delete_deduction(self, deduction_id:int)->None:
        if deduction_id <= 0:
            raise DomainError("Invalid ID")
        d = self.uow.deduction_repo.get_deduction_type_by_id(deduction_id)
        if not d:
            raise DeductionNotFoundError(f"Deduction with id {deduction_id} not found")
        try:
            self.uow.deduction_repo.delete_deduction_type(d)
        except SQLAlchemyError as e:
            raise DomainError(f"Failed to delete deduction: {e}")
