from sqlalchemy import (
    Column, ForeignKey, Integer, String, DateTime, Numeric, 
    CheckConstraint, Index, Text, Boolean
)
from backend.database_setups.database_setup import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from decimal import Decimal

class TaxBracket(Base):
    """
    Represents a tax bracket for tiered/progressive tax calculations.
    Supports income tax brackets, age-based brackets, and other progressive schemes.
    """
    __tablename__ = "tax_brackets"
    
    __table_args__ = (
        CheckConstraint('min_amount >= 0', name='check_min_positive'),
        CheckConstraint('max_amount IS NULL OR max_amount > min_amount', name='check_bracket_range'),
        CheckConstraint('rate >= 0 AND rate <= 100', name='check_rate_valid'),
        Index('ix_tax_bracket_tax_id', 'tax_id'),
        Index('ix_tax_bracket_min_max', 'min_amount', 'max_amount'),
    )
    
    # === PRIMARY & FOREIGN KEYS ===
    id = Column(Integer, primary_key=True, autoincrement=True)
    tax_id = Column(Integer, ForeignKey("tax.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # === BRACKET DEFINITION ===
    min_amount = Column(Numeric(12, 2), nullable=False)  # Lower limit of bracket
    max_amount = Column(Numeric(12, 2), nullable=True)  # Upper limit (NULL = open-ended)
    rate = Column(Numeric(5, 2), nullable=False)  # Tax rate as percentage (0-100)
    
    # === BRACKET DETAILS ===
    description = Column(Text, nullable=True)  # e.g., "First 100,000 KES at 10%"
    deductible_amount = Column(Numeric(12, 2), nullable=True, default=Decimal('0.00'))  # Standard deduction for bracket
    
    # === EFFECTIVE DATES ===
    effective_from = Column(DateTime, nullable=False, default=datetime.utcnow)
    effective_to = Column(DateTime, nullable=True)  # NULL = currently valid
    
    # === TIMESTAMPS ===
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # === RELATIONSHIPS ===
    tax_rule = relationship("Tax", back_populates="brackets")
    
    def __repr__(self):
        return f"<TaxBracket(tax_id={self.tax_id}, {self.min_amount}-{self.max_amount}, rate={self.rate}%)>"
    
    @property
    def is_active(self) -> bool:
        """Check if bracket is currently active."""
        now = datetime.utcnow()
        return (self.effective_from <= now and 
                (self.effective_to is None or self.effective_to >= now))