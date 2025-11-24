from datetime import datetime
from decimal import Decimal
from enum import Enum as PyEnum
from backend.database_setups.database_setup import Base
from sqlalchemy import (
    Column, Integer, Numeric, Date, ForeignKey, String, DateTime, 
    JSON, Enum, Index, CheckConstraint, UniqueConstraint, Text, Boolean
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
    """
    Represents an employee's payroll record for a specific pay period.
    Uses Numeric(12, 2) for financial accuracy (decimal vs float).
    Includes audit trails and versioning for compliance.
    """
    __tablename__ = "payrolls"
    
    # Constraints
    __table_args__ = (
        CheckConstraint('pay_period_start <= pay_period_end', name='check_pay_period_valid'),
        CheckConstraint('basic_salary >= 0', name='check_basic_salary_positive'),
        CheckConstraint('adjusted_base_salary >= 0', name='check_adjusted_base_positive'),
        CheckConstraint('gross_salary >= 0', name='check_gross_positive'),
        CheckConstraint('total_deductions >= 0', name='check_deductions_positive'),
        CheckConstraint('tax_amount >= 0', name='check_tax_positive'),
        CheckConstraint('net_salary >= 0', name='check_net_positive'),
        CheckConstraint('gross_salary >= (total_deductions + tax_amount)', name='check_net_calculation'),
        Index('ix_payroll_employee_period', 'employee_id', 'pay_period_start', 'pay_period_end'),
        Index('ix_payroll_status_date', 'status', 'payment_date'),
        Index('ix_payroll_created_at', 'created_at'),
        UniqueConstraint('employee_id', 'pay_period_start', 'pay_period_end', 'version',
                        name='uq_payroll_employee_period_version'),
    )
    
    # === PRIMARY KEYS & FOREIGN KEYS ===
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="RESTRICT"), nullable=False, index=True)
    
    # === PAY PERIOD INFORMATION ===
    pay_period_start = Column(Date, nullable=False, index=True)
    pay_period_end = Column(Date, nullable=False)
    payment_date = Column(Date, nullable=False, index=True)
    
    # === SALARY COMPONENTS (using Numeric for precision) ===
    basic_salary = Column(Numeric(12, 2), nullable=False)  # Position's base salary
    department_multiplier = Column(Numeric(5, 2), nullable=False, default=Decimal('1.00'))
    position_grade_multiplier = Column(Numeric(5, 2), nullable=False, default=Decimal('1.00'))
    adjusted_base_salary = Column(Numeric(12, 2), nullable=False)  # After multipliers
    
    # === EARNINGS ===
    total_allowances = Column(Numeric(12, 2), nullable=False, default=Decimal('0.00'))
    allowances_breakdown = Column(JSON, nullable=True)  # {allowance_name: amount}
    
    # === GROSS SALARY ===
    gross_salary = Column(Numeric(12, 2), nullable=False)
    
    # === DEDUCTIONS ===
    total_deductions = Column(Numeric(12, 2), nullable=False, default=Decimal('0.00'))
    deductions_breakdown = Column(JSON, nullable=True)  # {deduction_name: amount}
    
    # === TAXES ===
    tax_amount = Column(Numeric(12, 2), nullable=False, default=Decimal('0.00'))
    tax_breakdown = Column(JSON, nullable=True)  # {tax_type: amount} for detailed tax info
    
    # === NET SALARY ===
    net_salary = Column(Numeric(12, 2), nullable=False)
    
    # === PAYMENT & STATUS TRACKING ===
    status = Column(Enum(PayrollStatus), nullable=False, default=PayrollStatus.DRAFT, index=True)
    payment_method = Column(Enum(PaymentMethod), nullable=True)
    bank_transaction_id = Column(String(100), nullable=True)  # Reference ID from bank
    bank_transaction_reference = Column(String(255), nullable=True)  # For audit trail
    
    # === VERSIONING & AUDIT ===
    version = Column(Integer, nullable=False, default=1)  # For tracking amendments
    is_amended = Column(Boolean, nullable=False, default=False)
    amendment_reason = Column(Text, nullable=True)
    amended_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # User who amended
    
    # === TIMESTAMPS ===
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)  # When actually processed
    paid_at = Column(DateTime, nullable=True)  # When payment confirmed
    
    # === ADDITIONAL METADATA ===
    notes = Column(Text, nullable=True)  # Additional notes/comments
    processing_errors = Column(JSON, nullable=True)  # Track any processing errors
    
    # === RELATIONSHIPS ===
    employee = relationship("Employee", back_populates="payrolls")
    allowances = relationship("Allowance", back_populates="payroll", cascade="all, delete-orphan")
    deductions = relationship("Deduction", back_populates="payroll", cascade="all, delete-orphan")
    amended_by_user = relationship("User", foreign_keys=[amended_by])
    
    def __repr__(self):
        return f"<Payroll(id={self.id}, employee_id={self.employee_id}, period={self.pay_period_start}, status={self.status})>"
    
    @property
    def is_paid(self) -> bool:
        """Check if payroll has been paid."""
        return self.status == PayrollStatus.PAID
    
    @property
    def is_locked(self) -> bool:
        """Check if payroll is locked (cannot be modified)."""
        return self.status in [PayrollStatus.PAID, PayrollStatus.REVERSED, PayrollStatus.CANCELLED]
    
    def can_be_amended(self) -> bool:
        """Determine if payroll can still be amended."""
        return not self.is_locked and self.status != PayrollStatus.PROCESSED