from app.core.unit_of_work import UnitOfWork
from app.models.department_model import Department
from app.models.Position_model import Position
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.department_schema import DepartmentCreate
from app.domain.exceptions.base import DomainError
from app.domain.rules import department_rules

class DepartmentService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def add_department(self, payload: DepartmentCreate) -> Department:
        """Create a new department."""
        existing = self.uow.department_repo.get_department_by_name(payload.name)
        department_rules.ensure_no_duplicate_department(existing, payload.name)

        new = Department(**payload.model_dump())
        with self.uow:
            department = self.uow.department_repo.save_department(new)
            return department
        
            
       

    def get_positions_by_department(self, department_id: int) -> List[Position]:
        """Get all positions in a department."""
        department = self.uow.department_repo.get_department_by_id(department_id)
        if not department:
            raise DomainError(f"Department {department_id} not found")
        return self.uow.department_repo.get_positions_by_department(department_id)


    def get_all_departments(self) -> List[Department]:
        """Get all departments."""
        return self.uow.department_repo.get_all_departments()

    def delete_department(self, department_id: int) -> None:
        """Delete a department by ID."""
        department = self.uow.department_repo.get_department_by_id(department_id)
        if not department:
            raise DomainError(f"Department with id {department_id} not found")
        with self.uow:
            self.uow.department_repo.delete_department(department)
    

            
