from dataclasses import dataclass
from decimal import Decimal
from datetime import date
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.employee_salary_repository import EmployeeSalaryRepository
from app.repositories.position_salary_repository import PositionSalaryRepository
from app.exceptions.exceptions import SalaryNotFoundError, SalaryServiceError


@dataclass
class SalaryDTO:
    amount: Decimal
    currency: str
    pay_frequency: str


class SalaryService:
    """Service responsible for resolving the effective salary for an employee.

    - Uses repositories for DB access (no direct ORM queries here)
    - Implements precedence logic: employee salary overrides position salary
    - Returns a SalaryDTO (plain dataclass) suitable for engines
    """

    def __init__(self, db):
        self.employee_repo = EmployeeRepository(db)
        self.emp_salary_repo = EmployeeSalaryRepository(db)
        self.pos_salary_repo = PositionSalaryRepository(db)

    def resolve(self, employee_id: int, as_of_date: date) -> SalaryDTO:
        if employee_id <= 0:
            raise SalaryServiceError("Invalid employee id")

        employee = self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise SalaryNotFoundError(f"Employee {employee_id} not found")

        # 1) Try employee salary
        emp_salary = self.emp_salary_repo.get_active(employee_id, as_of_date)
        if emp_salary:
            return SalaryDTO(amount=emp_salary.amount, currency=emp_salary.currency, pay_frequency=emp_salary.salary_type.value)

        # 2) Fall back to position salary if employee has position
        if getattr(employee, "position_id", None):
            pos_salary = self.pos_salary_repo.get_active(employee.position_id, as_of_date)
            if pos_salary:
                return SalaryDTO(amount=pos_salary.amount, currency=pos_salary.currency, pay_frequency=pos_salary.salary_type.value)

        # 3) Nothing found
        raise SalaryNotFoundError(f"No effective salary for employee {employee_id} on {as_of_date}")
