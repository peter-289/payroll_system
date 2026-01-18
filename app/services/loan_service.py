from sqlalchemy.orm import Session
from app.models.Loans_advances_model import Loan
from sqlalchemy.exc import SQLAlchemyError
from app.domain.exceptions.base import LoanServiceError, LoanNotFoundError


class LoanService:
    def __init__(self, db: Session):
        self.db = db

    def create_loan(self, payload):
        loan = Loan(
            employee_id=getattr(payload, 'employee_id', None),
            type=getattr(payload, 'type', None),
            principle_amount=getattr(payload, 'principle_amount', None),
            balance_amount=getattr(payload, 'balance_amount', None),
            installment_amount=getattr(payload, 'installment_amount', None),
            interest_rate=getattr(payload, 'interest_rate', None),
            start_date=getattr(payload, 'start_date', None),
            end_date=getattr(payload, 'end_date', None),
            status=getattr(payload, 'status', None),
            description=getattr(payload, 'description', None)
        )
        try:
            self.db.add(loan)
            self.db.commit()
            self.db.refresh(loan)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise LoanServiceError(f"Failed to create loan: {e}")
        return loan

    def get_loan(self, loan_id:int):
        l = self.db.query(Loan).filter(Loan.id == loan_id).first()
        if not l:
            raise LoanNotFoundError(f"Loan with id {loan_id} not found")
        return l
    
    def get_employee_loan(self, employee_id:int):
        if employee_id <=0:
            raise LoanServiceError("Invalid id")
        loan = self.db.query(Loan).filter(Loan.employee_id == employee_id).first()
        if not loan:
            raise LoanNotFoundError(f"Loan with employee id: {employee_id} not found")
        return loan

    def list_loans(self, skip:int=0, limit:int=100):
        return self.db.query(Loan).offset(skip).limit(limit).all()

    def delete_loan(self, loan_id:int):
        l = self.db.query(Loan).filter(Loan.id == loan_id).first()
        if not l:
            raise LoanNotFoundError(f"Loan with id {loan_id} not found")
        try:
            self.db.delete(l)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise LoanServiceError(f"Failed to delete loan: {e}")
        return {"message":"Loan deleted successfully"}