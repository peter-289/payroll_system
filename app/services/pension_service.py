from sqlalchemy.orm import Session
from app.models.pension_model import Pension
from sqlalchemy.exc import SQLAlchemyError
from app.domain.exceptions.base import PensionServiceError, PensionNotFoundError


class PensionService:
    def __init__(self, db: Session):
        self.db = db

    def create_pension(self, payload):
        pension = Pension(
            employee_id=payload.employee_id,
            scheme_name=payload.scheme_name,
            pension_number=payload.pension_number,
            employer_contribution_percentage=payload.employer_contribution_percentage,
            employee_contribution_percentage=payload.employee_contribution_percentage,
            monthly_contribution=payload.monthly_contribution,
            start_date=getattr(payload, 'start_date', None)
        )
        try:
            self.db.add(pension)
            self.db.commit()
            self.db.refresh(pension)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise PensionServiceError(f"Failed to create pension: {e}")
        return pension

    def get_pension(self, pension_id:int):
        p = self.db.query(Pension).filter(Pension.id == pension_id).first()
        if not p:
            raise PensionNotFoundError(f"Pension with id {pension_id} not found")
        return p
    
    def get_employee_pension(self, employee_id:int):
        if employee_id<=0:
            raise PensionServiceError("Invalid ID")
        pension = self.db.query(Pension).filter(Pension.employee_id == employee_id).first()
        if not pension:
            raise PensionNotFoundError(f"Pension with employee id: {employee_id} not found.")
        return pension


    def list_pensions(self, skip: int = 0, limit: int = 100):
        return self.db.query(Pension).offset(skip).limit(limit).all()

    def delete_pension(self, pension_id:int):
        p = self.db.query(Pension).filter(Pension.id == pension_id).first()
        if not p:
            raise PensionNotFoundError(f"Pension with id {pension_id} not found")
        try:
            self.db.delete(p)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise PensionServiceError(f"Failed to delete pension: {e}")
        return {"message":"Pension deleted successfully"}