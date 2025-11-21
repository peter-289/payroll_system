from backend.database_setups.database_setup import Base
from sqlalchemy import Column, Integer, String, Float,Boolean, Text, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime




class AllowanceType(Base):
    __tablename__ = "allowance_types"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)   # "Housing Allowance"
    code = Column(String(20), unique=True, nullable=False)    # "HOUS"
    is_taxable = Column(Boolean, default=True)
    default_amount = Column(Numeric(12, 2), nullable=True)
    
    allowances = relationship("Allowance", back_populates="allowance_type")


class Allowance(Base):
    __tablename__ = "allowances"

    id = Column(Integer, primary_key=True)
    payroll_id = Column(Integer, ForeignKey("payrolls.id"), nullable=False)
    allowance_type_id = Column(Integer, ForeignKey("allowance_types.id"), nullable=False)
    name = Column(String(100), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    payroll = relationship("Payroll", back_populates="allowances")
    allowance_type = relationship("AllowanceType", back_populates="allowances")
