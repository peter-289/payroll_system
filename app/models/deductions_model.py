from app.db.database_setup import Base
from sqlalchemy import (
    Column, Integer, String, Numeric, DateTime, ForeignKey, 
    Boolean, func, Enum
)
from sqlalchemy.orm import relationship
from app.domain.enums import DeductionStatus


class DeductionType(Base):
    __tablename__ = "deduction_types"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)     # "PAYE", "NHIF", "NSSF Employee"
    code = Column(String(20), unique=True, nullable=False)      # "PAYE", "NHIF", "NSSF_EMP"
    is_statutory = Column(Boolean, default=False)               # True for legal deductions
    is_taxable = Column(Boolean, default=False)                 # Does it reduce taxable income?
    has_brackets = Column(Boolean, default=False)
    status =  Column(Enum(DeductionStatus), default=DeductionStatus.ACTIVE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now())  # True for tiered (PAYE, NHIF)

    deductions = relationship("Deduction", back_populates="deduction_type")
    brackets = relationship("DeductionBracket", back_populates="deduction_type")


class DeductionBracket(Base):
    __tablename__ = "deduction_brackets"
    id = Column(Integer, primary_key=True, index=True)
    deduction_type_id = Column(Integer, ForeignKey("deduction_types.id"))
    min_amount = Column(Numeric(14, 2))
    max_amount = Column(Numeric(14, 2), nullable=True)
    rate = Column(Numeric(5, 2))           # percentage
    fixed_amount = Column(Numeric(14, 2), nullable=True)

    deduction_type = relationship("DeductionType", back_populates="brackets")
    
    
class Deduction(Base):
    __tablename__ = "deductions"

    id = Column(Integer, primary_key=True, index=True)
    payroll_id = Column(Integer, ForeignKey("payrolls.id"), nullable=False)
    deduction_type_id = Column(Integer, ForeignKey("deduction_types.id"), nullable=False)
    amount = Column(Numeric(14, 2), nullable=False)
    is_percentage = Column(Boolean, default=False)

    payroll = relationship("Payroll", back_populates="deductions")
    deduction_type = relationship("DeductionType", back_populates="deductions")