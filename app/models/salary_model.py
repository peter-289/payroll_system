from app.db.database_setup import Base
from sqlalchemy import Column, Integer, Float, Enum, DateTime, ForeignKey, Numeric, String
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy.orm import relationship

class PayFrequency(str, PyEnum):
    MONTHLY = "monthly"
    HOURLY = "hourly"

class PositionSalary(Base):
    __tablename__ = "position_salaries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=False)
    salary_type = Column(Enum(PayFrequency), nullable=False, default=PayFrequency.MONTHLY)
    amount = Column(Numeric, nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    effective_from = Column(DateTime, default=datetime.utcnow)
    effective_to = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    #========================================================================================
    # Relationships can be defined here if needed
    #========================================================================================
    position = relationship("Position", back_populates="salaries")
    user = relationship("User", back_populates="position_salaries")
    #updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class EmployeeSalary(Base):
    __tablename__ = "employee_salaries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    salary_type = Column(Enum(PayFrequency), nullable=False, default=PayFrequency.MONTHLY)
    amount = Column(Numeric, nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    effective_from = Column(DateTime, default=datetime.utcnow)
    effective_to = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    #========================================================================================
    # Relationships can be defined here if needed
    #========================================================================================
    employee = relationship("Employee", back_populates="salaries")
    user = relationship("User", back_populates="employee_salaries")
    #updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)