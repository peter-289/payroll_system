from sqlalchemy.orm import Session
from app.models.department_model import Department
from app.models.Position_model import Position
from fastapi import HTTPException
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.department_schema import DepartmentCreate


class DepartmentService:
    def __init__(self, db: Session):
        self.db = db
    
    def say_hello_to_manager(self, name:str):
        print(f"Hello {name} what are you looking for here?")

    def add_department(self, payload:DepartmentCreate):
        department = self.db.query(Department).filter(Department.name == payload.name).first()
        if  department:
            raise HTTPException(status_code=400, detail=f"Department with name:{payload.name} already exists!")
        new = Department(**payload.model_dump())
        try:
            self.db.add(new)
            self.db.commit()
            self.db.refresh(new)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed: {e}!")
        return new

    def get_positions_by_department(self, department_id: int) -> List[Position]:
        department = self.db.query(Department).filter(Department.id == department_id).first()
        if not department:
            raise HTTPException(status_code=404, detail=f"Department {department_id} not found!")
        positions = self.db.query(Position).filter(Position.department_id == department.id).all()
        return positions
    
    def get_all_departments(self) -> List[Department]:
        departments = self.db.query(Department).all()
        return departments
    
    def delete_department(self, department_id:int):
        department = self.db.query(Department).filter(Department.id == department_id).first()
        if not department:
            raise HTTPException(status_code=404, detail=f"Department with id {department_id} not found!")
        try:
            self.db.delete(department)
            self.db.commit()
            return {"message":f"Department with id:{department_id} deleted successfully!"}
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to delete department with id {department_id}!")