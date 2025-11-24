from backend.database_setups.database_setup import Base
from sqlalchemy import (
    Column, Integer, String, DateTime, Enum, Numeric, ForeignKey, 
    Date, Index, CheckConstraint, Boolean, Text
)
from datetime import datetime
import enum
from sqlalchemy.orm import relationship
from decimal import Decimal

class TaxType(enum.Enum):
    """Tax calculation methods."""
    PERCENTAGE = "percentage"  # Fixed percentage of income
    FIXED = "fixed"  # Fixed amount per period
    TIERED = "tiered"  # Progressive brackets (e.g., income tax)
    GRADUATED = "graduated"  # Based on salary grade

class TaxStatus(enum.Enum):
    """Tax rule status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"

class Tax(Base):
    """
    Tax rule/configuration for payroll calculations.
    Supports multiple tax types and effective date management.
    """
    __tablename__ = "tax"
    
    __table_args__ = (
        CheckConstraint('effective_date IS NULL OR expiry_date IS NULL OR effective_date <= expiry_date', 
                       name='check_tax_date_range'),
        Index('ix_tax_code', 'tax_code'),
        Index('ix_tax_status', 'status'),
        Index('ix_tax_effective_date', 'effective_date'),
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # === TAX IDENTIFICATION ===
    tax_code = Column(String(20), unique=True, nullable=False, index=True)  # e.g., "PAYE", "NSSF"
    name = Column(String(100), nullable=False)  # e.g., "Personal Income Tax"
    description = Column(Text, nullable=True)
    
    # === TAX CONFIGURATION ===
    tax_type = Column(Enum(TaxType), nullable=False, default=TaxType.PERCENTAGE)
    
    # Tax limits and thresholds
    annual_exemption = Column(Numeric(12, 2), nullable=True, default=Decimal('0.00'))  # Tax-free threshold
    max_annual_tax = Column(Numeric(12, 2), nullable=True)  # Cap on annual tax (if applicable)
    is_cumulative = Column(Boolean, default=False)  # Whether tax is cumulative annually
    
    # === EFFECTIVE DATES ===
    effective_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    expiry_date = Column(DateTime, nullable=True)  # NULL = currently active indefinitely
    
    # === STATUS & AUDIT ===
    status = Column(Enum(TaxStatus), nullable=False, default=TaxStatus.ACTIVE)
    is_mandatory = Column(Boolean, default=True)  # Whether legally required
    is_deductible = Column(Boolean, default=False)  # Whether can be deducted from gross
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # === RELATIONSHIPS ===
    brackets = relationship("TaxBracket", back_populates="tax_rule", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Tax(id={self.id}, code={self.tax_code}, name={self.name}, type={self.tax_type})>"
    
    @property
    def is_active(self) -> bool:
        """Check if tax rule is currently active."""
        now = datetime.utcnow()
        return (self.status == TaxStatus.ACTIVE and 
                self.effective_date <= now and 
                (self.expiry_date is None or self.expiry_date >= now))




