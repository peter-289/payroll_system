"""Repository for managing Deduction and DeductionType entities in the database."""
from sqlalchemy.orm import Session
from app.models.deductions_model import Deduction, DeductionType, DeductionBracket
from typing import Optional, List
from decimal import Decimal


class DeductionRepository:
    """Repository for deduction database operations.
    
    Handles CRUD operations for Deduction entities and their types, including
    retrieval by ID, payroll, and deduction type.
    """
    def __init__(self, db: Session):
        """Initialize the deduction repository.
        
        Args:
            db: SQLAlchemy session for database operations.
        """
        self.db = db

    def save_deduction(self, deduction: Deduction) -> Deduction:
        """Save a new deduction to the database.
        
        Args:
            deduction: Deduction instance to save.
            
        Returns:
            The saved Deduction instance.
        """
        self.db.add(deduction)
        return deduction

    def update_deduction(self, deduction: Deduction) -> Deduction:
        """Update an existing deduction record.
        
        Args:
            deduction: Deduction instance with updated values.
            
        Returns:
            The updated Deduction instance.
        """
        return deduction

    def get_deduction_by_id(self, deduction_id: int) -> Optional[Deduction]:
        """Retrieve a deduction by ID.
        
        Args:
            deduction_id: The deduction's ID.
            
        Returns:
            Deduction instance if found, None otherwise.
        """
        return self.db.query(Deduction).filter(Deduction.id == deduction_id).first()

    def get_deductions_by_payroll(self, payroll_id: int) -> List[Deduction]:
        """Retrieve all deductions for a payroll record.
        
        Args:
            payroll_id: The payroll record's ID.
            
        Returns:
            List of Deduction instances associated with the payroll.
        """
        return self.db.query(Deduction).filter(Deduction.payroll_id == payroll_id).all()

    def get_deductions_by_type(self, deduction_type_id: int) -> List[Deduction]:
        """Retrieve all deductions of a specific type.
        
        Args:
            deduction_type_id: The deduction type's ID.
            
        Returns:
            List of Deduction instances of the specified type.
        """
        return self.db.query(Deduction).filter(Deduction.deduction_type_id == deduction_type_id).all()

    def delete_deduction(self, deduction: Deduction) -> None:
        """Delete a deduction from the database.
        
        Args:
            deduction: Deduction instance to delete.
        """
        self.db.delete(deduction)

    def save_deduction_type(self, deduction_type: DeductionType) -> DeductionType:
        """Save a new deduction type to the database.
        
        Args:
            deduction_type: DeductionType instance to save.
            
        Returns:
            The saved DeductionType instance.
        """
        self.db.add(deduction_type)
        self.db.flush()
        return deduction_type

    def update_deduction_type(self, deduction_type: DeductionType) -> DeductionType:
        """Update an existing deduction type record.
        
        Args:
            deduction_type: DeductionType instance with updated values.
            
        Returns:
            The updated DeductionType instance.
        """
        self.db.merge(deduction_type)
        return deduction_type
    
    def get_deduction_type_by_id(self, id: int) -> Optional[DeductionType]:
        """Retrieve a deduction type by ID.
        
        Args:
            id: The deduction type's ID.
            
        Returns:
            DeductionType instance if found, None otherwise.
        """
        return self.db.query(DeductionType).filter(DeductionType.id == id).first()
    

    def get_taxable_deduction_type(self, id: int) -> Optional[DeductionType]:
        """Retrieve a taxable deduction type by ID.
        
        Args:
            id: The deduction type's ID.
            
        Returns:
            DeductionType instance if it's taxable and found, None otherwise.
        """
        return self.db.query(DeductionType).filter(DeductionType.id == id).order_by(DeductionType.is_taxable).first()

    def get_deduction_type_by_code(self, code: str) -> Optional[DeductionType]:
        """Retrieve a deduction type by code.
        
        Args:
            code: The unique deduction code.
            
        Returns:
            DeductionType instance if found, None otherwise.
        """
        return self.db.query(DeductionType).filter(DeductionType.code == code).first()


    def get_all_deduction_types(self) -> List[DeductionType]:
        """Retrieve all deduction types.
        
        Returns:
            List of all DeductionType instances in the database.
        """
        return self.db.query(DeductionType).all()


    def delete_deduction_type(self, deduction_type: DeductionType) -> None:
        """Delete a deduction type from the database.
        
        Args:
            deduction_type: DeductionType instance to delete.
        """
        self.db.delete(deduction_type)
        

    def save_deduction_bracket(self, bracket: DeductionBracket) -> DeductionBracket:
        """Save a new deduction bracket to the database.
        
        Args:
            bracket: DeductionBracket instance to save.
            
        Returns:
            The saved DeductionBracket instance.
        """
        self.db.add(bracket)
        return bracket
    

    def get_brackets_by_type(self, id: int) -> List[DeductionBracket]:
        """Retrieve all brackets for a deduction type.
        
        Args:
            id: The deduction type's ID.
            
        Returns:
            List of DeductionBracket instances for the specified type.
        """
        return self.db.query(DeductionBracket).filter(DeductionBracket.deduction_type_id == id).all()
    
    
    def get_bracket_for_amount(self, id: int, amount: Decimal) -> Optional[DeductionBracket]:
        """Retrieve the appropriate bracket for a given amount in a deduction type.
        
        Args:
            id: The deduction type's ID.
            amount: The amount to find the appropriate bracket for.
            
        Returns:
            DeductionBracket instance if found, None otherwise.
        """
        return self.db.query(DeductionBracket).filter(
            DeductionBracket.deduction_type_id == id,
            DeductionBracket.min_amount <= amount,
            (DeductionBracket.max_amount.is_(None) | (DeductionBracket.max_amount >= amount))
        ).first()


    def get_deduction_by_name(self, name: str) -> Optional[DeductionType]:
        """Retrieve a deduction type by name.
        
        Args:
            name: The deduction type's name.
            
        Returns:
            DeductionType instance if found, None otherwise.
        """
        return self.db.query(DeductionType).filter(DeductionType.name == name).first()
