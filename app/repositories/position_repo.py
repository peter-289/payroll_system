from sqlalchemy.orm import Session
from typing import Optional
from app.models.Position_model import Position
from app.models.department_model import Department
from app.repositories.department_repo import DepartmentRepository


class PositionRepository:
    def __init__(self, db: Session):
        self.db = db
        self.department_repo = DepartmentRepository(db)

    def get_position(self, position_title: str)->Optional[Position]:
        return self.db.query(Position).filter(Position.title == position_title).first()
    
    
    def positions_department(self, department_id:int)->Optional[Position]:
        """
        Get a position belonging to a department
        """
        position = self.db.query(Position).filter(Position.department_id == department_id).first()
        return position
        

        
