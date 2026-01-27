from app.core.unit_of_work import UnitOfWork
from app.models.salary_model import EmployeeSalary, PositionSalary, PayFrequency
from app.domain.exceptions.base import DomainError, SalaryNotFoundError
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date
from app.models.Position_model import Position
from sqlalchemy.orm import joinedload


class SalaryService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def get_employee_salary(self, employee_id: int, position_id:int):
        if employee_id <= 0:
            raise DomainError("Invalid employee ID")
        try:
            # query employee-specific salaries first (by employee_id)
            salary = self.uow.session.query(EmployeeSalary).filter(EmployeeSalary.employee_id == employee_id).order_by(EmployeeSalary.effective_from.desc()).first()
            if not salary:
                # fallback to the current position salary if available
                salary = self.get_current_position_salary(position_id)
                if not salary:
                    raise SalaryNotFoundError(f"Salary not found for employee {employee_id}")
        
        except SQLAlchemyError as e:
            raise DomainError(f"DB error fetching salary: {e}")
        return salary.amount

    def get_effective_employee_salary(self, employee_id: int, target_date: date):
        if employee_id <= 0:
            raise DomainError("Invalid employee ID")
        try:
            salary = self.uow.session.query(EmployeeSalary).filter(
                EmployeeSalary.employee_id == employee_id,
            ).filter(EmployeeSalary.effective_from <= target_date)
            salary = salary.filter((EmployeeSalary.effective_to == None) | (EmployeeSalary.effective_to >= target_date))
            salary = salary.order_by(EmployeeSalary.effective_from.desc()).first()
        except SQLAlchemyError as e:
            raise DomainError(f"DB error finding effective salary: {e}")
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
            self.uow.session.add(salary)
            self.uow.session.commit()
            self.uow.session.refresh(salary)
        except SQLAlchemyError as e:
            self.uow.session.rollback()
            raise DomainError(f"Failed to add employee salary: {e}")
        return salary

    def get_position_salaries(self, position_id:int):
        if position_id <= 0:
            raise DomainError("Invalid position ID")
        try:
            result = self.uow.session.query(PositionSalary).filter(PositionSalary.position_id == position_id).order_by(PositionSalary.effective_from).all()
        except SQLAlchemyError as e:
            raise DomainError(f"DB error fetching position salaries: {e}")
        return result
    
    def get_current_position_salary(self, position_id: int) -> PositionSalary | None:
       if position_id <= 0:
            raise DomainError("Invalid position ID")
       try:
            position_salary = self.uow.session.query(PositionSalary).filter(
                 PositionSalary.position_id == position_id,
                 PositionSalary.effective_from <= date.today(),
             ).filter(
                 (PositionSalary.effective_to == None) | (PositionSalary.effective_to >= date.today())
             ).order_by(PositionSalary.effective_from.desc()).first()
       except SQLAlchemyError as e:
           raise DomainError(f"DB error fetching current position salary: {e}")
       return position_salary
    

    def add_position_salary(self, position_id:int, amount:float, salary_type:PayFrequency = PayFrequency.MONTHLY, effective_from:datetime|None=None, created_by:int|None=None):
        if position_id <= 0:
            raise DomainError("Invalid position ID")
        position = self.uow.session.query(Position).filter(Position.id == position_id).first()
        if not position:
            raise DomainError(f"Position with ID {position_id} does not exist")
        effective_from = effective_from or datetime.utcnow()
        position_salary = PositionSalary(
            position_id=position_id,
            amount=amount,
            salary_type=salary_type,
            effective_from=effective_from,
            created_by=created_by or 0
        )
        try:
            self.uow.session.add(position_salary)
            self.uow.session.commit()
            self.uow.session.refresh(position_salary)
        except SQLAlchemyError as e:
            self.uow.session.rollback()
            raise DomainError(f"Failed to add position salary: {e}")
        return position_salary
