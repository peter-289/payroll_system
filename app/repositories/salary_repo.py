from sqlalchemy.orm import Session
from app.models.salary_model import PositionSalary as Salary

class SalaryRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, salary) -> None:
        self.db.add(salary)

    def update(self, salary) -> None:
        return salary

    def get_salary_by_employee_id(self, employee_id: int):
        return self.db.query(Salary).filter(Salary.employee_id == employee_id).first()

