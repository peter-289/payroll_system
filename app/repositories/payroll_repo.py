"""
Repository for Payroll operations.
"""

from sqlalchemy.orm import Session
from app.models.payroll_model import Payroll
from typing import List


class PayrollRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payroll: Payroll) -> Payroll:
        self.db.add(payroll)
        

        return payroll

    def get_by_id(self, payroll_id: int) -> Payroll:
        return self.db.query(Payroll).filter(Payroll.id == payroll_id).first()

    def get_by_employee(self, employee_id: int) -> List[Payroll]:
        return self.db.query(Payroll).filter(Payroll.employee_id == employee_id).all()

    def update(self, payroll: Payroll) -> Payroll:
        

        return payroll
