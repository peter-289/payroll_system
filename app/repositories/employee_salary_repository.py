from datetime import date
from sqlalchemy.orm import Session
from app.models.salary_model import EmployeeSalary


class EmployeeSalaryRepository:
    """Repository for employee salaries. No business logic here."""

    def __init__(self, db: Session):
        self.db = db

    def get_active(self, employee_id: int, as_of_date: date) -> EmployeeSalary | None:
        """Return the active EmployeeSalary for employee on as_of_date or None."""
        if employee_id <= 0:
            return None
        q = (
            self.db.query(EmployeeSalary)
            .filter(EmployeeSalary.employee_id == employee_id)
            .filter(EmployeeSalary.effective_from <= as_of_date)
            .filter((EmployeeSalary.effective_to == None) | (EmployeeSalary.effective_to >= as_of_date))
            .order_by(EmployeeSalary.effective_from.desc())
        )
        return q.first()
