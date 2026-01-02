from sqlalchemy.orm import Session
from app.models.deductions_model import Deduction, DeductionType, DeductionBracket
from app.exceptions.exceptions import DeductionServiceError, DeductionNotFoundError
from sqlalchemy.exc import SQLAlchemyError
from app.utils.tax_bracket_validator import validate_no_overlaps


class DeductionService:
    def __init__(self, db: Session):
        self.db = db
    
    def _generate_deduction_code(self, name: str) -> str:
        import uuid
        prefix = name[:3].upper()
        unique_suffix = uuid.uuid4().hex[:6].upper()
        code = f"{prefix}-{unique_suffix}"
        return code
    
    def create_deduction_brackets(self, deduction_type_id: int, brackets: list)-> None:
        validate_no_overlaps(brackets)
        for bracket in brackets:
            db_bracket = DeductionBracket(
                deduction_type_id=deduction_type_id,
                min_amount=bracket.min_amount,
                max_amount=bracket.max_amount,
                rate=bracket.rate,
                fixed_amount=bracket.fixed_amount
            )
            self.db.add(db_bracket)

    def create_deduction(self, payload):
        """Create a DeductionType with optional brackets"""
        code = self._generate_deduction_code(payload.name)
        if self.db.query(DeductionType).filter(DeductionType.name == payload.name).first():
            raise DeductionServiceError(f"Deduction with name {payload.name} already exists")
        deduction = DeductionType(
            name=payload.name,
            code=code,
            is_statutory=payload.is_statutory,
            is_taxable=payload.is_taxable,
            has_brackets=payload.has_brackets
        )
        try:
            self.db.add(deduction)
            self.db.flush()

            if payload.has_brackets and getattr(payload, 'brackets', None):
                self.create_deduction_brackets(deduction.id, payload.brackets)

            self.db.commit()
            self.db.refresh(deduction)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DeductionServiceError(f"Failed to create deduction: {e}")
        return deduction

    def get_deduction(self, deduction_id: int):
        d = self.db.query(DeductionType).filter(DeductionType.id == deduction_id).order_by(DeductionType.is_taxable).first()
        if not d:
            raise DeductionNotFoundError(f"Deduction with id {deduction_id} not found")
        return d

    def list_deductions(self, skip: int = 0, limit: int = 100):
        return self.db.query(DeductionType).offset(skip).limit(limit).all()

    def update_deduction(self, deduction_id: int, payload):
        d = self.db.query(DeductionType).filter(DeductionType.id == deduction_id).first()
        if not d:
            raise DeductionNotFoundError(f"Deduction with id {deduction_id} not found")

        # Prevent duplicate names
        if payload.name and payload.name != d.name:
            if self.db.query(DeductionType).filter(DeductionType.name == payload.name).first():
                raise DeductionServiceError(f"Deduction with name {payload.name} already exists")

        try:
            d.name = payload.name
            d.is_statutory = payload.is_statutory
            d.is_taxable = payload.is_taxable
            d.has_brackets = payload.has_brackets

            # Handle brackets
            if d.has_brackets and getattr(payload, 'brackets', None):
                validate_no_overlaps(payload.brackets)
                # remove existing brackets
                self.db.query(DeductionBracket).filter(DeductionBracket.deduction_type_id == d.id).delete()
                self.db.flush()
                # create new ones
                self.create_deduction_brackets(d.id, payload.brackets)
            elif not d.has_brackets:
                # remove any existing brackets if switching off
                self.db.query(DeductionBracket).filter(DeductionBracket.deduction_type_id == d.id).delete()

            self.db.commit()
            self.db.refresh(d)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DeductionServiceError(f"Failed to update deduction: {e}")
        return d

    def delete_deduction(self, deduction_id:int):
        d = self.db.query(DeductionType).filter(DeductionType.id == deduction_id).first()
        if not d:
            raise DeductionNotFoundError(f"Deduction with id {deduction_id} not found")
        try:
            self.db.delete(d)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DeductionServiceError(f"Failed to delete deduction: {e}")
        return {"message":"Deduction type deleted successfully"}