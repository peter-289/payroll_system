from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.database_setups.database_setup import Base
from datetime import datetime




class EmployeeBankAccount(Base):
    __tablename__ = "employee_bank_accounts"

    account_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False)
    bank_name = Column(String(100), nullable=False)
    account_number = Column(String(30), nullable=False)
    account_type = Column(String(20), nullable=True)  # e.g., Savings, Checking
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String(20), default="active")  # e.g., active, inactive

    
    # relationships
    employee = relationship("Employee", back_populates="bank_accounts")