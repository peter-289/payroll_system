from sqlalchemy import (
    Column, ForeignKey, Integer, DateTime, Numeric, 
    Text
)
from app.db.database_setup import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from decimal import Decimal


class TaxBracket(Base):
    """
    Represents a tax bracket for tiered/progressive tax calculations.
    Supports income tax brackets, age-based brackets, and other progressive schemes.
    """
    __tablename__ = "tax_brackets"
    
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tax_id = Column(Integer, ForeignKey("tax.id", ondelete="CASCADE"), nullable=False, index=True)
    min_amount = Column(Numeric(12, 2), nullable=False)  # Lower limit of bracket
    max_amount = Column(Numeric(12, 2), nullable=True)  # Upper limit (NULL = open-ended)
    rate = Column(Numeric(5, 2), nullable=False)  # Tax rate as percentage (0-100)
    description = Column(Text, nullable=True)  # e.g., "First 100,000 KES at 10%"
    deductible_amount = Column(Numeric(12, 2), nullable=True, default=Decimal('0.00'))  # Standard deduction for bracket
    effective_from = Column(DateTime, nullable=False, default=datetime.utcnow)
    effective_to = Column(DateTime, nullable=True)  # NULL = currently valid
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # === RELATIONSHIPS ===
    tax_rule = relationship("Tax", back_populates="brackets")
    
    
   