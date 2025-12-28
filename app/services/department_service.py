from sqlalchemy.orm import Session
from app.models.department_model import Department
from app.models.Position_model import Position
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.department_schema import DepartmentCreate
from app.exceptions.exceptions import DepartmentServiceError, DepartmentAlreadyExistsError


class DepartmentService:
    def __init__(self, db: Session):
        self.db = db

    def add_department(self, payload: DepartmentCreate) -> Department:
        """Create a new department."""
        department = self.db.query(Department).filter(Department.name == payload.name).first()
        if department:
            raise DepartmentAlreadyExistsError(f"Department with name '{payload.name}' already exists")
        
        new = Department(**payload.model_dump())
        try:
            self.db.add(new)
            self.db.commit()
            self.db.refresh(new)
            return new
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DepartmentServiceError(f"Failed to create department: {str(e)}")

    def get_positions_by_department(self, department_id: int) -> List[Position]:
        """Get all positions in a department."""
        department = self.db.query(Department).filter(Department.id == department_id).first()
        if not department:
            raise DepartmentServiceError(f"Department {department_id} not found")
        positions = self.db.query(Position).filter(Position.department_id == department.id).all()
        return positions
    
    
    def get_all_departments(self) -> List[Department]:
        """Get all departments."""
        departments = self.db.query(Department).all()
        return departments
    
    def delete_department(self, department_id: int) -> None:
        """Delete a department by ID."""
        department = self.db.query(Department).filter(Department.id == department_id).first()
        if not department:
            raise DepartmentServiceError(f"Department with id {department_id} not found")
        try:
            self.db.delete(department)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DepartmentServiceError(f"Failed to delete department: {str(e)}")
