from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from backend.database_setups.database_setup import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from enum import Enum


class CoverageType(str, Enum):
    HEALTH = "health"
    DENTAL = "dental"
    VISION = "vision"
    LIFE = "life"
    DISABILITY = "disability"

class InsuranceStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class Insurance(Base):
    __tablename__ = 'insurances'

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    insurance_provider = Column(String, nullable=False)
    policy_number = Column(String, nullable=False, unique=True)
    coverage_type = Column(String, nullable=False, default=CoverageType.LIFE.value)
    premium_amount = Column(Integer, nullable=False)
    employer_contribution = Column(Integer, nullable=False)
    employee_contribution = Column(Integer, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    status = Column(String, default=InsuranceStatus.ACTIVE.value)

    employee = relationship("Employee", back_populates="insurances")


