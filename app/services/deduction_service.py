from app.models.deductions_model import DeductionType, DeductionBracket
from app.domain.rules import deduction_rules
from app.domain.exceptions.base import DomainError, DeductionNotFoundError
from app.utils.tax_bracket_validator import validate_no_overlaps
import uuid
from app.core.unit_of_work import UnitOfWork
from app.domain.rules.domain_rules import validate_id
from app.domain.rules.deduction_rules import ensure_no_duplicate_deduction_type
from typing import Optional

class DeductionService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
    
    def _generate_deduction_code(self, name: str) -> str:
        """
        Docstring for _generate_deduction_code
        
        :param self: References the class instance
        :param name: Accepts a name argument
        :type name: str
        :return: Returns a unique code generated from the first 3 letters of the name
        :rtype: str
        """
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
        validate_id(type_id)
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
        
        :param self: References the class instance
        :param payload: Payload containing deduction type details
        :type payload: Any
        :return: Returns the created DeductionType instance
        :rtype: DeductionType
        """

        code = self._generate_deduction_code(payload.name)
        existing = self.uow.deduction_repo.get_deduction_by_name(payload.name)
        deduction_rules.check_unique_names(payload.name, existing.name if existing else "")

        deduction = DeductionType(
            name=payload.name,
            code=code,
            is_statutory=payload.is_statutory,
            is_taxable=payload.is_taxable,
            has_brackets=payload.has_brackets
           )
        with self.uow:
             saved_deduction = self.uow.deduction_repo.save_deduction_type(deduction)
             if payload.has_brackets:
                if not payload.brackets:
                   raise DomainError("Brackets must be provided for deductions with brackets")
                self.create_deduction_brackets(saved_deduction.id, payload.brackets)
                return saved_deduction
       

    def get_taxable_deduction(self, id: int)-> DeductionType:
        validate_id(id)
        deduction_type = self.uow.deduction_repo.get_taxable_deduction_type(id)
        if not deduction_type:
            raise DeductionNotFoundError(f"Deduction with id {id} not found")
        return deduction_type


    def list_deductions(self, skip: int = 0, limit: int = 100):
        all_deductions = self.uow.deduction_repo.get_all_deduction_types()
        return all_deductions[skip:skip + limit]

    def update_deduction(self, deduction_id: int, payload):
        validate_id(deduction_id)
       
        existing = self.uow.deduction_repo.get_deduction_type_by_id(deduction_id)
        if not existing:
            raise DeductionNotFoundError(f"Deduction with id {deduction_id} not found")
        
     
        ensure_no_duplicate_deduction_type(existing, payload.name)

        
        existing.name = payload.name
        existing.is_statutory = payload.is_statutory
        existing.is_taxable = payload.is_taxable
        existing.has_brackets = payload.has_brackets

            
        if existing.has_brackets and getattr(payload, 'brackets', None):
                validate_no_overlaps(payload.brackets)
                with self.uow:
                    deduction_type = self.uow.deduction_repo.get_deduction_type_by_id(existing.id)
                    self.uow.deduction_repo.delete_deduction_type(deduction_type)
                    self.create_deduction_brackets(existing.id, payload.brackets)
        elif not existing.has_brackets:
                with self.uow:
                     self.uow.deduction_repo.delete_deduction_type(deduction_type)  
                     updated_deduction = self.uow.deduction_repo.update_deduction_type(existing)
                     return  updated_deduction  


    def get_deduction(self, deduction_id: int)-> Optional[DeductionType]:  
        """
        Docstring for get_deduction
        
        :param self: Refernces the class instance
        :param deduction_id: A unique id integer
        :type deduction_id: int
        :return: Returns a deductiontype object or none
        :rtype: DeductionType | None
        """
        validate_id(deduction_id)
        deduction_type = self.uow.deduction_repo.get_deduction_type_by_id(deduction_id)
        if not deduction_type:
            raise DeductionNotFoundError("Deductiontype not found")
        return deduction_type



    def delete_deduction(self, deduction_id:int)->None:
        validate_id(deduction_id)
        d = self.uow.deduction_repo.get_deduction_type_by_id(deduction_id)
        if not d:
            raise DeductionNotFoundError(f"Deduction with id {deduction_id} not found")
        with self.uow:
            self.uow.deduction_repo.delete_deduction_type(d)
       