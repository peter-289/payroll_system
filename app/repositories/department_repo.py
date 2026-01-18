from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.department_model import Department
from app.models.Position_model import Position


class DepartmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_department(self, department: Department) -> Department:
        self.db.add(department)
        self.db.commit()
        self.db.refresh(department)
        return department

    def update_department(self, department: Department) -> Department:
        self.db.commit()
        self.db.refresh(department)
        return department

    def get_department_by_id(self, department_id: int) -> Optional[Department]:
        return self.db.query(Department).filter(Department.id == department_id).first()

    def get_department_by_name(self, department_name: str) -> Optional[Department]:
        return self.db.query(Department).filter(Department.name == department_name).first()

    def get_all_departments(self) -> List[Department]:
        return self.db.query(Department).all()

    def delete_department(self, department: Department) -> None:
        self.db.delete(department)
        self.db.commit()

    # Position related methods
    def get_positions_by_department(self, department_id: int) -> List[Position]:
        return self.db.query(Position).filter(Position.department_id == department_id).all()
    
   