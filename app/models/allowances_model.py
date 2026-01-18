from app.db.database_setup import Base
from sqlalchemy import (
    Column, Integer, String, Numeric, Text, DateTime, ForeignKey, Boolean,
    Index, CheckConstraint, Enum, func
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.domain.enums import AllowanceStatus, AllowanceCalculationType, AllowancePercentageBasis


class AllowanceType(Base):
    """
    Defines allowance types and policies.
    Centralizes allowance configuration for consistency and maintainability.
    """
    __tablename__ = "allowance_types"
    
    __table_args__ = (
        Index('ix_allowance_code', 'code'),
        Index('ix_allowancetype_status', 'status'),
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_taxable = Column(Boolean, default=True)
    is_recurring = Column(Boolean, default=True)
    calculation_type = Column(Enum(AllowanceCalculationType),nullable=False, default=AllowanceCalculationType.FIXED)  
    percentage_of = Column(Enum(AllowancePercentageBasis), nullable=True )  
    default_amount = Column(Numeric(12, 2), nullable=True)  
    max_amount = Column(Numeric(12, 2), nullable=True)  
    min_amount = Column(Numeric(12, 2), nullable=True)  
    status = Column(Enum(AllowanceStatus), nullable=False, default=AllowanceStatus.ACTIVE)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

 
    # === RELATIONSHIPS ===
    allowances = relationship("Allowance", back_populates="allowance_type", cascade="all, delete-orphan")
    
    

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
        
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    payroll_id = Column(Integer, ForeignKey("payrolls.id", ondelete="CASCADE"), nullable=False, index=True)
    allowance_type_id = Column(Integer, ForeignKey("allowance_types.id", ondelete="RESTRICT"), nullable=False)
    name = Column(String(100), nullable=False)
    code = Column(String(20), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    is_taxable = Column(Boolean, default=True)
    calculation_basis = Column(String(255), nullable=True, comment="Human readable explanation") 
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    
    # === RELATIONSHIPS ===
    payroll = relationship("Payroll", back_populates="allowances")
    allowance_type = relationship("AllowanceType", back_populates="allowances")
    
    