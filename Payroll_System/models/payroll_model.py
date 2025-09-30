from datetime import datetime
from database import Base
from sqlalchemy import Column, Integer, Float, Date, ForeignKey, text
from sqlalchemy.orm import relationship

class Payroll(Base):
    __tablename__ = "payrolls"
    
    payroll_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    pay_period_start = Column(Date, nullable=False)
    pay_period_end = Column(Date, nullable=False)
    basic_salary = Column(Float, nullable=False)
    gross_salary = Column(Float, nullable=False)
    total_deductions = Column(Float, nullable=False)
    net_salary = Column(Float, nullable=False)
    payment_date = Column(Date, nullable=False)
    status = Column(text, nullable=False)  # e.g., Paid, Pending, Failed
    bank_transaction_id = Column(Integer, ForeignKey("bank_transactions.transaction_id"), nullable=False)
    created_at = Column(Date, default=datetime.utcnow)
    updated_at = Column(Date, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships
    employee = relationship("Employee", back_populates="payrolls")  
    #bank_transaction = relationship("BankTransaction", back_populates="payrolls")
