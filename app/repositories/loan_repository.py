from app.models.Loans_advances_model import Loan
from sqlalchemy.orm import Session

class LoanRepository:
    def __init__(self, db: Session ):
        self.db = db



    def save_loan(self, loan: Loan) -> Loan:
        self.db.add(loan)
        return loan
    
    def get_load_by_id(self, loan_id: int) -> Loan:
        loan = self.db.query(Loan).filter(Loan.id == loan_id).first()
        return loan