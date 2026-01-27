from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from app.models.employee_model import Employee

class EmployeeRepository:
    """Repository for managing Employee entities."""
    def __init__(self, db: Session):
        self.db = db


    def add_and_flush(self, employee: Employee) -> Employee:
        """Save a new Employee instance to the database and flush the session."""
        self.db.add(employee)
        self.db.flush()
        return employee
    

    def update(self, employee: Employee) -> Employee:
        """Update an existing Employee instance in the database."""
        self.db.merge(employee)
        self.db.flush()
        return employee
    

    def get_by_id(self, employee_id: int) -> Optional[Employee]:
        """Retrieve an Employee by ID, including related User, Department, and Position."""
        return (
            self.db.query(Employee)
            .options(joinedload(Employee.user), joinedload(Employee.department), joinedload(Employee.position))
            .filter(Employee.id == employee_id)
            .first()
        )


    def get_all_employees(self, skip: int = 0, limit: Optional[int] = None) -> List[Employee]:
        """Retrieve all Employees with optional pagination, including related User, Department, and Position."""
        query = self.db.query(Employee).options(joinedload(Employee.user), joinedload(Employee.department), joinedload(Employee.position)).offset(skip)
        if limit:
            query = query.limit(limit)
        return query.all()


    def get_by_user_id(self, user_id: int) -> Optional[Employee]:
        """Retrieve an Employee by associated User ID."""
        return self.db.query(Employee).filter(Employee.user_id == user_id).first()

    def delete(self, employee: Employee) -> None:
        """Delete an Employee instance from the database."""
        self.db.delete(employee)
        return None

    def find_by_username(self, username: str):
        """Find an Employee by their associated User's username."""
        # This is a convenience helper for validations
        from app.models.user_model import User
        return self.db.query(User).filter(User.username == username).first()


