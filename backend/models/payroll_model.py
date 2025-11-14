from datetime import datetime
from backend.database_setups.database_setup import Base
from sqlalchemy import Column, Integer, Float, Date, ForeignKey, String, DateTime, JSON
from sqlalchemy.orm import relationship

class Payroll(Base):
    __tablename__ = "payrolls"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    pay_period_start = Column(Date, nullable=False)
    pay_period_end = Column(Date, nullable=False)
    basic_salary = Column(Float, nullable=False)  # Position's base salary
    department_multiplier = Column(Float, nullable=False, default=1.0)  # Salary multiplier from department
    position_grade_multiplier = Column(Float, nullable=False, default=1.0)  # Multiplier based on position grade
    adjusted_base_salary = Column(Float, nullable=False)  # Basic salary after applying multipliers
    allowances_breakdown = Column(JSON)  # Detailed breakdown of allowances
    deductions_breakdown = Column(JSON)  # Detailed breakdown of deductions
    gross_salary = Column(Float, nullable=False)
    total_deductions = Column(Float, nullable=False)
    net_salary = Column(Float, nullable=False)
    payment_date = Column(Date, nullable=False)
    status = Column(String, nullable=False)  # e.g., Paid, Pending, Failed
    bank_transaction_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships
    employee = relationship("Employee", back_populates="payrolls")  
    allowances = relationship("Allowance", back_populates="payroll")
    deductions = relationship("Deduction", back_populates="payroll")
    
   