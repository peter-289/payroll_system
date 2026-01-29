"""Repository for managing User entities in the database."""
from app.models.user_model import User
from sqlalchemy.orm import Session
from typing import Optional

class UserRepository:
    """Repository for user database operations.
    
    Handles CRUD operations for User entities including retrieval by ID or username.
    """
    def __init__(self, db: Session):
        """Initialize the user repository.
        
        Args:
            db: SQLAlchemy session for database operations.
        """
        self.db = db

    def save(self, user: User) -> User:
        """Save a new user to the database.
        
        Args:
            user: User instance to save.
            
        Returns:
            The saved User instance.
        """
        self.db.add(user)
        self.db.flush()
        return user
    
    def update(self, user: User) -> User:
        """Update an existing user record.
        
        Args:
            user: User instance with updated values.
            
        Returns:
            The updated User instance.
        """
        return user
    
    def get_user(self, username: str) -> Optional[User]:
        """Retrieve a user by username.
        
        Args:
            username: The username to search for.
            
        Returns:
            User instance if found, None otherwise.
        """
        return self.db.query(User).filter(User.username == username).first()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve a user by ID.
        
        Args:
            user_id: The user's ID.
            
        Returns:
            User instance if found, None otherwise.
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def delete(self, user: User) -> None:
        """Delete a user from the database.
        
        Args:
            user: User instance to delete.
        """
        self.db.delete(user)
