from sqlalchemy.orm import Session
from typing import Optional
from app.models.employee_bank_account import EmployeeBankAccount


class BankDetailsRepository:
    """Repository for managing employee bank details."""
    def __init__(self, db: Session):
        self.db = db

    def get_account(self, account_number: str)->Optional[EmployeeBankAccount]:
        return self.db.query(EmployeeBankAccount).filter(EmployeeBankAccount.account_number == account_number).first()

    def save(self, bank_account: EmployeeBankAccount) -> None:
        """Save a new or existing EmployeeBankAccount instance to the database."""
        self.db.add(bank_account)
        
