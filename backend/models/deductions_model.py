from backend.database_setups.database_setup import Base
from sqlalchemy import (
    Column, Integer, String, Numeric, Date, Text, DateTime, ForeignKey, 
    Index, CheckConstraint, Enum, Boolean
)
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from decimal import Decimal

class DeductionType(PyEnum):
    """Types of deductions for tax compliance."""
    STATUTORY = "statutory"  # Tax, NSSF, etc.
    VOLUNTARY = "voluntary"  # Loans, insurance, union dues
    DISCIPLINARY = "disciplinary"  # Penalties, advances
    COURT_ORDER = "court_order"  # Garnishments

class DeductionStatus(PyEnum):
    """Status of deductions."""
    ACTIVE = "active"
    COMPLETED = "completed"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"

class Deduction(Base):
    """
    Represents a deduction from employee payroll.
    Supports recurring deductions, caps, and audit trails.
    """
    __tablename__ = "deductions"
    
    __table_args__ = (
        CheckConstraint('amount >= 0', name='check_deduction_amount_positive'),
        CheckConstraint('max_amount IS NULL OR max_amount >= 0', name='check_max_deduction_positive'),
        Index('ix_deduction_payroll_id', 'payroll_id'),
        Index('ix_deduction_type_code', 'deduction_code'),
        Index('ix_deduction_status', 'status'),
    )
    
    # === PRIMARY & FOREIGN KEYS ===
    id = Column(Integer, primary_key=True, autoincrement=True)
    payroll_id = Column(Integer, ForeignKey("payrolls.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # === DEDUCTION DETAILS ===
    deduction_code = Column(String(20), nullable=False, index=True)  # e.g., "NSSF", "TAX", "UNION"
    name = Column(String(100), nullable=False)  # e.g., "National Social Security Fund"
    description = Column(Text, nullable=True)
    deduction_type = Column(Enum(DeductionType), nullable=False, default=DeductionType.STATUTORY)
    
    # === AMOUNT DETAILS ===
    amount = Column(Numeric(12, 2), nullable=False)  # Amount deducted this period
    max_amount = Column(Numeric(12, 2), nullable=True)  # Monthly/annual cap (optional)
    
    # === TRACKING & COMPLIANCE ===
    reference_number = Column(String(100), nullable=True)  # e.g., Loan ID, court order number
    status = Column(Enum(DeductionStatus), nullable=False, default=DeductionStatus.ACTIVE)
    is_taxable = Column(Boolean, default=False)  # Whether deduction reduces taxable income
    
    # === RECURRING DEDUCTION INFO ===
    is_recurring = Column(Boolean, default=False)
    recurring_end_date = Column(Date, nullable=True)
    
    # === TIMESTAMPS & AUDIT ===
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # === RELATIONSHIPS ===
    payroll = relationship("Payroll", back_populates="deductions")
    
    def __repr__(self):
        return f"<Deduction(id={self.id}, code={self.deduction_code}, amount={self.amount})>"
