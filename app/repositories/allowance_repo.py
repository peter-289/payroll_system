"""Repository for managing Allowance and AllowanceType entities in the database."""
from sqlalchemy.orm import Session
from app.models.allowances_model import Allowance, AllowanceType
from typing import Optional, List
from app.domain.enums import AllowanceStatus


class AllowanceRepository:
    """Repository for allowance database operations.
    
    Handles CRUD operations for Allowance entities and their types, including
    retrieval by ID, payroll, and allowance type.
    """
    def __init__(self, db: Session):
        """Initialize the allowance repository.
        
        Args:
            db: SQLAlchemy session for database operations.
        """
        self.db = db

    def save_allowance(self, allowance: Allowance) -> Allowance:
        """Save a new allowance to the database.
        
        Args:
            allowance: Allowance instance to save.
            
        Returns:
            The saved Allowance instance.
        """
        self.db.add(allowance)
        return allowance

    def update_allowance(self, allowance: Allowance) -> Allowance:
        """Update an existing allowance record.
        
        Args:
            allowance: Allowance instance with updated values.
            
        Returns:
            The updated Allowance instance.
        """
        return allowance
    
    def get_allowance_by_id(self, allowance_id: int) -> Optional[Allowance]:
        """Retrieve an allowance by ID.
        
        Args:
            allowance_id: The allowance's ID.
            
        Returns:
            Allowance instance if found, None otherwise.
        """
        return self.db.query(Allowance).filter(Allowance.id == allowance_id).first()
    
    def get_allowance_by_type(self, allowance_type_id: int) -> Optional[Allowance]:
        """Retrieve an allowance by allowance type ID.
        
        Args:
            allowance_type_id: The allowance type's ID.
            
        Returns:
            Allowance instance if found, None otherwise.
        """
        return self.db.query(Allowance).filter(
            Allowance.allowance_type_id == allowance_type_id
        ).first()

    def get_allowances_by_payroll(self, payroll_id: int) -> List[Allowance]:
        """Retrieve all allowances for a payroll record.
        
        Args:
            payroll_id: The payroll record's ID.
            
        Returns:
            List of Allowance instances associated with the payroll.
        """
        return self.db.query(Allowance).filter(Allowance.payroll_id == payroll_id).all()

    def get_all_allowances(self) -> List[Allowance]:
        """Retrieve all allowances.
        
        Returns:
            List of all Allowance instances in the database.
        """
        return self.db.query(Allowance).all()

    def get_allowances_by_type(self, allowance_type_id: int) -> List[Allowance]:
        """Retrieve all allowances of a specific type.
        
        Args:
            allowance_type_id: The allowance type's ID.
            
        Returns:
            List of Allowance instances of the specified type.
        """
        return self.db.query(Allowance).filter(Allowance.allowance_type_id == allowance_type_id).all()

    def delete_allowance(self, allowance: Allowance) -> None:
        """Delete an allowance from the database.
        
        Args:
            allowance: Allowance instance to delete.
        """
        self.db.delete(allowance)

# ============================================================================================
# ------------------ ALLOWANCE TYPE METHODS --------------------------------------------------
    def save_allowance_type(self, allowance_type: AllowanceType) -> AllowanceType:
        self.db.add(allowance_type)
        

        return allowance_type
    
    def roll_back(self):
        self.db.rollback()

    def update_allowance_type(self, allowance_type: AllowanceType) -> AllowanceType:
        

        return allowance_type

    def get_allowance_type_by_id(self, id: int) -> Optional[AllowanceType]:
        return self.db.query(AllowanceType).filter(AllowanceType.id == id).first()

    def get_allowance_type_by_code(self, code: str, name: str) -> Optional[AllowanceType]:
        return self.db.query(AllowanceType).filter(AllowanceType.code == code, AllowanceType.name == name).first()

    def get_all_allowance_types(self, active_only: bool = True) -> List[AllowanceType]:
        query = self.db.query(AllowanceType)
        if active_only:
            query = query.filter(AllowanceType.status == AllowanceStatus.ACTIVE)
        return query.all()

    def delete_allowance_type(self, allowance_type: AllowanceType) -> None:
        self.db.delete(allowance_type)
        
    
    
