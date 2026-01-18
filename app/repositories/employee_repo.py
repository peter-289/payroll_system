from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from app.models.employee_model import Employee

class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def temp_save(self, employee: Employee) -> Employee:
        self.db.add(employee)
        self.db.flush()
        return employee
    
    def update(self, employee: Employee) -> Employee:
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def get_by_id(self, employee_id: int) -> Optional[Employee]:
        return (
            self.db.query(Employee)
            .options(joinedload(Employee.user), joinedload(Employee.department), joinedload(Employee.position))
            .filter(Employee.id == employee_id)
            .first()
        )

    def get_all(self, skip: int = 0, limit: Optional[int] = None) -> List[Employee]:
        query = self.db.query(Employee).options(joinedload(Employee.user), joinedload(Employee.department), joinedload(Employee.position)).offset(skip)
        if limit:
            query = query.limit(limit)
        return query.all()

    def get_by_user_id(self, user_id: int) -> Optional[Employee]:
        return self.db.query(Employee).filter(Employee.user_id == user_id).first()

    def delete(self, employee: Employee) -> None:
        self.db.delete(employee)
        self.db.commit()
        return None

    def find_by_username(self, username: str):
        # convenience helper for validations
        from app.models.user_model import User
        return self.db.query(User).filter(User.username == username).first()


