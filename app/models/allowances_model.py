from app.db.database_setup import Base
from sqlalchemy import (
    Column, Integer, String, Numeric, Text, DateTime, ForeignKey, Boolean,
    Index, CheckConstraint, Enum, Date
)
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from decimal import Decimal

class AllowanceStatus(PyEnum):
    """Status of allowance."""
    ACTIVE = "active"
    COMPLETED = "completed"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"

class AllowanceType(Base):
    """
    Defines allowance types and policies.
    Centralizes allowance configuration for consistency and maintainability.
    """
    __tablename__ = "allowance_types"
    
    __table_args__ = (
        Index('ix_allowance_code', 'code'),
        Index('ix_allowancetype_is_active', 'is_active'),
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(20), unique=True, nullable=False, index=True)  # e.g., "HOUS", "TRANS", "MEAL"
    name = Column(String(100), unique=True, nullable=False)  # e.g., "Housing Allowance"
    description = Column(Text, nullable=True)
    is_taxable = Column(Boolean, default=True)  # Whether included in taxable income
    is_recurring = Column(Boolean, default=True)  # Whether paid every period
    is_percentage_based = Column(Boolean, default=False)  # If true, calculated as % of salary
    percentage_of = Column(String(50), nullable=True)  # e.g., "basic_salary", "gross_salary"
    default_amount = Column(Numeric(12, 2), nullable=True)  # Suggested amount
    max_amount = Column(Numeric(12, 2), nullable=True)  # Maximum allowed per period
    min_amount = Column(Numeric(12, 2), nullable=True)  # Minimum allowed per period
    is_active = Column(Enum(AllowanceStatus), nullable=False, default=AllowanceStatus.ACTIVE)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # === RELATIONSHIPS ===
    allowances = relationship("Allowance", back_populates="allowance_type", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<AllowanceType(id={self.id}, code={self.code}, name={self.name})>"


class Allowance(Base):
    """
    Individual allowance record for a specific payroll period.
    Stores actual amounts paid for audit and compliance purposes.
    """
    __tablename__ = "allowances"
    
    __table_args__ = (
        CheckConstraint('amount >= 0', name='check_allowance_amount_positive'),
        Index('ix_allowance_payroll_id', 'payroll_id'),
        Index('ix_allowance_type_id', 'allowance_type_id'),
        Index('ix_allowance_status', 'status'),
    )
    
    # === PRIMARY & FOREIGN KEYS ===
    id = Column(Integer, primary_key=True, autoincrement=True)
    payroll_id = Column(Integer, ForeignKey("payrolls.id", ondelete="CASCADE"), nullable=False, index=True)
    allowance_type_id = Column(Integer, ForeignKey("allowance_types.id", ondelete="RESTRICT"), nullable=False)
    name = Column(String(100), nullable=False)  # Copy of allowance_type name for historical accuracy
    code = Column(String(20), nullable=False)  # Copy of allowance_type code
    amount = Column(Numeric(12, 2), nullable=False)  # Actual amount for this payroll
    description = Column(Text, nullable=True)
    is_taxable = Column(Boolean, default=True)  # Whether taxable (cached from type)
    calculation_basis = Column(String(255), nullable=True)  # e.g., "50% of basic", "Fixed amount"
    status = Column(Enum(AllowanceStatus), nullable=False, default=AllowanceStatus.ACTIVE)
    reference_number = Column(String(100), nullable=True)  # External reference if applicable
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # === RELATIONSHIPS ===
    payroll = relationship("Payroll", back_populates="allowances")
    allowance_type = relationship("AllowanceType", back_populates="allowances")
    
    def __repr__(self):
        return f"<Allowance(id={self.id}, payroll_id={self.payroll_id}, name={self.name}, amount={self.amount})>"
