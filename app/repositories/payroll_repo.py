"""Repository for managing Payroll entities in the database."""

from sqlalchemy.orm import Session
from app.models.payroll_model import Payroll
from typing import List, Optional


class PayrollRepository:
    """Repository for payroll database operations.
    
    Handles CRUD operations for Payroll entities including creation, retrieval
    by employee, and updates.
    """
    def __init__(self, db: Session):
        """Initialize the payroll repository.
        
        Args:
            db: SQLAlchemy session for database operations.
        """
        self.db = db

    def create(self, payroll: Payroll) -> Payroll:
        """Create and save a new payroll record.
        
        Args:
            payroll: Payroll instance to create.
            
        Returns:
            The saved Payroll instance.
        """
        self.db.add(payroll)
        return payroll

    def get_by_id(self, payroll_id: int) -> Optional[Payroll]:
        """Retrieve a payroll record by ID.
        
        Args:
            payroll_id: The payroll record's ID.
            
        Returns:
            Payroll instance if found, None otherwise.
        """
        return self.db.query(Payroll).filter(Payroll.id == payroll_id).first()

    def get_by_employee(self, employee_id: int) -> List[Payroll]:
        """Retrieve all payroll records for an employee.
        
        Args:
            employee_id: The employee's ID.
            
        Returns:
            List of Payroll instances for the specified employee.
        """
        return self.db.query(Payroll).filter(Payroll.employee_id == employee_id).all()

    def update(self, payroll: Payroll) -> Payroll:
        """Update an existing payroll record.
        
        Args:
            payroll: Payroll instance with updated values.
            
        Returns:
            The updated Payroll instance.
        """
        return payroll
