from datetime import datetime
from decimal import Decimal
from enum import Enum as PyEnum
from backend.database_setups.database_setup import Base
from sqlalchemy import (
    Column, Integer, Numeric, UniqueConstraint,Date, ForeignKey, String, DateTime, 
    JSON, Enum, Text, Boolean
)
from sqlalchemy.orm import relationship

class PayrollStatus(PyEnum):
    """Enum for payroll processing states."""
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    PROCESSED = "processed"
    PAID = "paid"
    FAILED = "failed"
    REVERSED = "reversed"
    CANCELLED = "cancelled"

class PaymentMethod(PyEnum):
    """Supported payment methods."""
    BANK_TRANSFER = "bank_transfer"
    CHECK = "check"
    CASH = "cash"
    MOBILE_MONEY = "mobile_money"

class Payroll(Base):
  
    __tablename__ = "payrolls"
    
    unique_constraints = (
        UniqueConstraint("employee_id", "pay_period_start", "pay_period_end", name="uix_employee_pay_period"),
    )
    
    # --- Primary Keys & Relationships ---
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), index=True, nullable=False)

    # --- Pay Period ---
    pay_period_start = Column(Date, nullable=False, index=True)
    pay_period_end = Column(Date, nullable=False, index=True)
    payment_date = Column(Date, nullable=False)

    # --- Earnings Breakdown (inputs live in separate tables) ---
    total_allowances = Column(Numeric(12, 2), nullable=False, default=Decimal("0.00"))
    total_deductions = Column(Numeric(12, 2), nullable=False, default=Decimal("0.00"))
    tax_amount = Column(Numeric(12, 2), nullable=False, default=Decimal("0.00"))

    
    # --- Final Results ---
    gross_salary = Column(Numeric(12, 2), nullable=False)
    net_salary = Column(Numeric(12, 2), nullable=False)

    # --- Payment Info ---
    status = Column(Enum(PayrollStatus), nullable=False, default=PayrollStatus.DRAFT, index=True)
    payment_method = Column(Enum(PaymentMethod), nullable=True)
    bank_transaction_id = Column(String(100), nullable=True)
    bank_transaction_reference = Column(String(255), nullable=True)

    # --- Timestamps ---
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    paid_at = Column(DateTime, nullable=True)

    # --- Versioning & Audit ---
    version = Column(Integer, nullable=False, default=1)
    is_amended = Column(Boolean, default=False)
    amendment_reason = Column(Text, nullable=True)
    amended_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    

    # --- Misc ---
    notes = Column(Text, nullable=True)
    processing_errors = Column(JSON, nullable=True)
    
    # === RELATIONSHIPS ===
    employee = relationship("Employee", back_populates="payrolls")
    allowances = relationship("Allowance", back_populates="payroll", cascade="all, delete-orphan")
    deductions = relationship("Deduction", back_populates="payroll", cascade="all, delete-orphan")
    
    