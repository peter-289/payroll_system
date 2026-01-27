from sqlalchemy.orm import Session
from app.models.deductions_model import Deduction, DeductionType, DeductionBracket
from typing import Optional, List
from decimal import Decimal


class DeductionRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_deduction(self, deduction: Deduction) -> Deduction:
        self.db.add(deduction)
        

        return deduction

    def update_deduction(self, deduction: Deduction) -> Deduction:
        

        return deduction

    def get_deduction_by_id(self, deduction_id: int) -> Optional[Deduction]:
        return self.db.query(Deduction).filter(Deduction.id == deduction_id).first()

    def get_deductions_by_payroll(self, payroll_id: int) -> List[Deduction]:
        return self.db.query(Deduction).filter(Deduction.payroll_id == payroll_id).all()

    def get_deductions_by_type(self, deduction_type_id: int) -> List[Deduction]:
        return self.db.query(Deduction).filter(Deduction.deduction_type_id == deduction_type_id).all()

    def delete_deduction(self, deduction: Deduction) -> None:
        self.db.delete(deduction)
        

    # DeductionType methods
    def save_deduction_type(self, deduction_type: DeductionType) -> DeductionType:
        self.db.add(deduction_type)
        

        return deduction_type

    def update_deduction_type(self, deduction_type: DeductionType) -> DeductionType:
        

        return deduction_type
    
    def get_deduction_type_by_id(self, id: int) -> Optional[DeductionType]:
        return self.db.query(DeductionType).filter(DeductionType.id == id).first()
    
    def get_taxable_deduction_type(self, id: int)->Optional[DeductionType]:
        return self.db.query(DeductionType).filter(DeductionType.id == id).order_by(DeductionType.is_taxable).first()

    def get_deduction_type_by_code(self, code: str) -> Optional[DeductionType]:
        return self.db.query(DeductionType).filter(DeductionType.code == code).first()


    def get_all_deduction_types(self) -> List[DeductionType]:
        return self.db.query(DeductionType).all()

    def delete_deduction_type(self, deduction_type: DeductionType) -> None:
        self.db.delete(deduction_type)
        

    # DeductionBracket methods
    def save_deduction_bracket(self, bracket: DeductionBracket) -> DeductionBracket:
        self.db.add(bracket)
        

        return bracket
    

    def get_brackets_by_type(self, id: int) -> List[DeductionBracket]:
        return self.db.query(DeductionBracket).filter(DeductionBracket.deduction_type_id == id).all()


    def get_bracket_for_amount(self, id: int, amount: Decimal) -> Optional[DeductionBracket]:
        return self.db.query(DeductionBracket).filter(
            DeductionBracket.deduction_type_id == id,
            DeductionBracket.min_amount <= amount,
            (DeductionBracket.max_amount.is_(None) | (DeductionBracket.max_amount >= amount))
        ).first()


    def get_deduction_by_name(self, name: str)-> Optional[DeductionType]:
        """
        Docstring for get_deduction_by_name
        
        :param self: Description
        :param name: Description
        :type name: str
        :return: Description
        :rtype: DeductionType | None
        """
        return self.db.query(DeductionType).filter(DeductionType.name == name).first()
