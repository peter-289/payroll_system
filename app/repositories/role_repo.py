"""Repository for managing Role entities in the database."""
from app.models.roles_model import Role
from sqlalchemy.orm import Session
from typing import Optional

class RoleRepository:
    """Repository for role database operations.
    
    Handles retrieval of Role entities by ID or name.
    """
    def __init__(self, db: Session):
        """Initialize the role repository.
        
        Args:
            db: SQLAlchemy session for database operations.
        """
        self.db = db
    
    def get_role_by_id(self, role_id: int) -> Optional[Role]:
        """Retrieve a role by ID.
        
        Args:
            role_id: The role's ID.
            
        Returns:
            Role instance if found, None otherwise.
        """
        return self.db.query(Role).filter(Role.id == role_id).first()
    
    def get_role_by_name(self, rolename: str) -> Optional[Role]:
        """Retrieve a role by name.
        
        Args:
            rolename: The role's name.
            
        Returns:
            Role instance if found, None otherwise.
        """
        return self.db.query(Role).filter(Role.role_name == rolename).first()
