from sqlalchemy.orm import Session
from app.models.employee_model import Employee
from typing import Optional

class EmployeeRepository:
    def __init__(self, db:Session):
        self.db = db
    
    
    def get_employee(self, user_id:int)->Optional[Employee]:
        return self.db.query(Employee).filter(Employee.user_id == user_id).first()
      

