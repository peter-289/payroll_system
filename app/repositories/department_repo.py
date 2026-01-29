"""Repository for managing Department and Position entities in the database."""
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.department_model import Department
from app.models.Position_model import Position


class DepartmentRepository:
    """Repository for department and position database operations.
    
    Handles CRUD operations for Department entities and retrieval of positions
    within departments.
    """
    def __init__(self, db: Session):
        """Initialize the department repository.
        
        Args:
            db: SQLAlchemy session for database operations.
        """
        self.db = db

    def save_department(self, department: Department) -> Department:
        """Save a new department to the database.
        
        Args:
            department: Department instance to save.
            
        Returns:
            The saved Department instance.
        """
        self.db.add(department)
        return department

    def update_department(self, department: Department) -> Department:
        """Update an existing department record.
        
        Args:
            department: Department instance with updated values.
            
        Returns:
            The updated Department instance.
        """
        return department

    def get_department_by_id(self, department_id: int) -> Optional[Department]:
        """Retrieve a department by ID.
        
        Args:
            department_id: The department's ID.
            
        Returns:
            Department instance if found, None otherwise.
        """
        return self.db.query(Department).filter(Department.id == department_id).first()

    def get_department_by_name(self, department_name: str) -> Optional[Department]:
        """Retrieve a department by name.
        
        Args:
            department_name: The department's name.
            
        Returns:
            Department instance if found, None otherwise.
        """
        return self.db.query(Department).filter(Department.name == department_name).first()

    def get_all_departments(self) -> List[Department]:
        """Retrieve all departments.
        
        Returns:
            List of all Department instances in the database.
        """
        return self.db.query(Department).all()

    def delete_department(self, department: Department) -> None:
        """Delete a department from the database.
        
        Args:
            department: Department instance to delete.
        """
        self.db.delete(department)

    def get_positions_by_department(self, department_id: int) -> List[Position]:
        """Retrieve all positions within a department.
        
        Args:
            department_id: The department's ID.
            
        Returns:
            List of Position instances in the specified department.
        """
        return self.db.query(Position).filter(Position.department_id == department_id).all()
    
   
