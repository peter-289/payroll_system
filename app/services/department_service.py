from sqlalchemy.orm import Session
from app.models.department_model import Department
from app.models.Position_model import Position
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.department_schema import DepartmentCreate
from app.domain.exceptions.base import DepartmentServiceError
from app.domain.rules import department_rules

class DepartmentService:
    def __init__(self, db: Session):
        self.db = db

    def add_department(self, payload: DepartmentCreate) -> Department:
        """Create a new department."""
        existing = self.department_repo.get_department_by_name(payload.name)
        department_rules.ensure_no_duplicate_department(existing, payload.name)

        new = Department(**payload.model_dump())
        try:
            return self.department_repo.save_department(new)
        except SQLAlchemyError as e:
            raise DepartmentServiceError(f"Failed to create department: {str(e)}")

    def get_positions_by_department(self, department_id: int) -> List[Position]:
        """Get all positions in a department."""
        department = self.department_repo.get_department_by_id(department_id)
        if not department:
            raise DepartmentServiceError(f"Department {department_id} not found")
        return self.department_repo.get_positions_by_department(department_id)


    def get_all_departments(self) -> List[Department]:
        """Get all departments."""
        return self.department_repo.get_all_departments()

    def delete_department(self, department_id: int) -> None:
        """Delete a department by ID."""
        department = self.department_repo.get_department_by_id(department_id)
        if not department:
            raise DepartmentServiceError(f"Department with id {department_id} not found")
        try:
            self.department_repo.delete_department(department)
        except SQLAlchemyError as e:
            raise DepartmentServiceError(f"Failed to delete department: {str(e)}")
