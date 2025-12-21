from sqlalchemy.orm import Session
from app.models.salary_model import PositionSalary, EmployeeSalary, PayFrequency
from app.models.Position_model import Position
from datetime import date

class SalaryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_employee_salary(self, employee_id: int) -> EmployeeSalary:
        salary = self.db.query(EmployeeSalary).filter(EmployeeSalary.employee_id == employee_id).order_by(EmployeeSalary.effective_from.desc()).first()
        return salary 
    
    def effective_employee_salary(self, employee_id: int, target_date:date) -> EmployeeSalary:
        salary = self.db.query(EmployeeSalary).filter(
            EmployeeSalary.employee_id == employee_id)\
            .filter(EmployeeSalary.effective_from <= target_date)\
            .filter((EmployeeSalary.effective_to == None) | (EmployeeSalary.effective_to >= target_date))\
            .order_by(EmployeeSalary.effective_from.desc()).first()
        return salary
    
    def add_employee_salary(self, employee_salary: EmployeeSalary) -> EmployeeSalary:
        self.db.add(employee_salary)
        self.db.commit()
        self.db.refresh(employee_salary)
        return employee_salary
    
    def get_position_salaries(self, position_id: int):
        return self.db.query(PositionSalary)\
            .filter(PositionSalary.position_id == position_id)\
            .order_by(PositionSalary.effective_from)\
            .all()

    def find_effective_position_salary(self, position_id: int, target_date: date):
        return self.db.query(PositionSalary)\
            .filter(PositionSalary.position_id == position_id)\
            .filter(PositionSalary.effective_from <= target_date)\
            .filter((PositionSalary.effective_to == None) | (PositionSalary.effective_to >= target_date))\
            .order_by(PositionSalary.effective_from.desc())\
            .first()

    def add_position_salary(self, position_salary: PositionSalary):
        self.db.add(position_salary)
        self.db.commit()
        self.db.refresh(position_salary)
        return position_salary


