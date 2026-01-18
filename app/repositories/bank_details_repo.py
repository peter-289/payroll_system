from sqlalchemy.orm import Session
from typing import Optional
from app.models.employee_bank_account import EmployeeBankAccount


class BankRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_account(self, account_number: str)->Optional[EmployeeBankAccount]:
        return self.db.query(EmployeeBankAccount).filter(EmployeeBankAccount.account_number == account_number).first()