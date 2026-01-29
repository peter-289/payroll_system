"""Repository for managing Salary entities in the database."""
from sqlalchemy.orm import Session
from app.models.salary_model import PositionSalary as Salary
from typing import Optional


class SalaryRepository:
    """Repository for salary database operations.
    
    Handles CRUD operations for PositionSalary entities including retrieval
    by employee ID.
    """
    def __init__(self, db: Session):
        """Initialize the salary repository.
        
        Args:
            db: SQLAlchemy session for database operations.
        """
        self.db = db

    def save(self, salary: Salary) -> None:
        """Save a new salary record to the database.
        
        Args:
            salary: Salary instance to save.
        """
        self.db.add(salary)

    def update(self, salary: Salary) -> Salary:
        """Update an existing salary record.
        
        Args:
            salary: Salary instance with updated values.
            
        Returns:
            The updated Salary instance.
        """
        return salary

    def get_salary_by_employee_id(self, employee_id: int) -> Optional[Salary]:
        """Retrieve the salary record for an employee.
        
        Args:
            employee_id: The employee's ID.
            
        Returns:
            Salary instance if found, None otherwise.
        """
        return self.db.query(Salary).filter(Salary.employee_id == employee_id).first()

