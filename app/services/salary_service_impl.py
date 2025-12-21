from sqlalchemy.orm import Session
from app.models.salary_model import EmployeeSalary, PositionSalary, PayFrequency
from app.exceptions.exceptions import SalaryServiceError, SalaryNotFoundError
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date


class SalaryService:
    def __init__(self, db: Session):
        self.db = db

    def get_employee_salary(self, employee_id: int):
        try:
            salary = self.db.query(EmployeeSalary).filter(EmployeeSalary.employee_id == employee_id).order_by(EmployeeSalary.effective_from.desc()).first()
        except SQLAlchemyError as e:
            raise SalaryServiceError(f"DB error fetching salary: {e}")
        if not salary:
            raise SalaryNotFoundError(f"Salary not found for employee {employee_id}")
        return salary

    def get_effective_employee_salary(self, employee_id: int, target_date: date):
        try:
            salary = self.db.query(EmployeeSalary).filter(
                EmployeeSalary.employee_id == employee_id,
            ).filter(EmployeeSalary.effective_from <= target_date)
            salary = salary.filter((EmployeeSalary.effective_to == None) | (EmployeeSalary.effective_to >= target_date))
            salary = salary.order_by(EmployeeSalary.effective_from.desc()).first()
        except SQLAlchemyError as e:
            raise SalaryServiceError(f"DB error finding effective salary: {e}")
        if not salary:
            raise SalaryNotFoundError(f"No effective salary for employee {employee_id} on {target_date}")
        return salary

    def add_employee_salary(self, employee_id:int, amount:float, salary_type:PayFrequency = PayFrequency.MONTHLY, effective_from:datetime|None=None, created_by:int|None=None):
        effective_from = effective_from or datetime.utcnow()
        salary = EmployeeSalary(
            employee_id=employee_id,
            amount=amount,
            salary_type=salary_type,
            effective_from=effective_from,
            created_by=created_by or 0
        )
        try:
            self.db.add(salary)
            self.db.commit()
            self.db.refresh(salary)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SalaryServiceError(f"Failed to add employee salary: {e}")
        return salary

    def get_position_salaries(self, position_id:int):
        try:
            result = self.db.query(PositionSalary).filter(PositionSalary.position_id == position_id).order_by(PositionSalary.effective_from).all()
        except SQLAlchemyError as e:
            raise SalaryServiceError(f"DB error fetching position salaries: {e}")
        return result

    def add_position_salary(self, position_id:int, amount:float, salary_type:PayFrequency = PayFrequency.MONTHLY, effective_from:datetime|None=None, created_by:int|None=None):
        effective_from = effective_from or datetime.utcnow()
        position_salary = PositionSalary(
            position_id=position_id,
            amount=amount,
            salary_type=salary_type,
            effective_from=effective_from,
            created_by=created_by or 0
        )
        try:
            self.db.add(position_salary)
            self.db.commit()
            self.db.refresh(position_salary)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SalaryServiceError(f"Failed to add position salary: {e}")
        return position_salary