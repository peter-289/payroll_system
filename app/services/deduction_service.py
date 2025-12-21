from sqlalchemy.orm import Session
from app.models.deductions_model import Deduction
from app.exceptions.exceptions import DeductionServiceError, DeductionNotFoundError
from sqlalchemy.exc import SQLAlchemyError


class DeductionService:
    def __init__(self, db: Session):
        self.db = db

    def create_deduction(self, payload):
        deduction = Deduction(
            deduction_code=payload.deduction_code if hasattr(payload, 'deduction_code') else payload.name[:8].upper(),
            name=payload.name,
            description=getattr(payload, 'description', None),
            payroll_id=getattr(payload, 'payroll_id', None),
            deduction_type=getattr(payload, 'type', None),
            amount=payload.amount,
            max_amount=getattr(payload, 'max_amount', None),
            status=getattr(payload, 'status', 'active'),
            is_taxable=getattr(payload, 'is_taxable', False),
            is_recurring=getattr(payload, 'is_recurring', False),
            recurring_end_date=getattr(payload, 'recurring_end_date', None)
        )
        try:
            self.db.add(deduction)
            self.db.commit()
            self.db.refresh(deduction)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DeductionServiceError(f"Failed to create deduction: {e}")
        return deduction

    def get_deduction(self, deduction_id: int):
        d = self.db.query(Deduction).filter(Deduction.id == deduction_id).first()
        if not d:
            raise DeductionNotFoundError(f"Deduction with id {deduction_id} not found")
        return d

    def list_deductions(self, skip: int = 0, limit: int = 100):
        return self.db.query(Deduction).offset(skip).limit(limit).all()

    def delete_deduction(self, deduction_id:int):
        d = self.db.query(Deduction).filter(Deduction.id == deduction_id).first()
        if not d:
            raise DeductionNotFoundError(f"Deduction with id {deduction_id} not found")
        try:
            self.db.delete(d)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DeductionServiceError(f"Failed to delete deduction: {e}")
        return {"message":"Deduction deleted successfully"}