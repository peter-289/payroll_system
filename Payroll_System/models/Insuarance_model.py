from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class Insurance(Base):
    __tablename__ = 'insurances'

    insurance_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.employee_id'), nullable=False)
    insurance_provider = Column(String, nullable=False)
    policy_number = Column(String, nullable=False, unique=True)
    coverage_type = Column(String, nullable=False)
    premium_amount = Column(Integer, nullable=False)
    employer_contribution = Column(Integer, nullable=False)
    employee_contribution = Column(Integer, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    status = Column(String, default='active')

    employee = relationship("Employee", back_populates="insurances")


