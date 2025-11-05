from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from backend.database_setups.database_setup import Base
import datetime
from sqlalchemy.orm import relationship

class Loan(Base):
    __tablename__ = 'loans'

    loan_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.employee_id'))
    type = Column(Text)
    principle_amount = Column(Integer)
    balance_amount = Column(Integer)
    installment_amount = Column(Integer)
    interest_rate = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(Text)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    employee = relationship("Employee", back_populates="loans")
