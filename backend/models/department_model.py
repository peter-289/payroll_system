from backend.database_setups.database_setup import Base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float
from datetime import datetime
from sqlalchemy.orm import relationship
from backend.models.employee_model import Employee


class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True)
    description = Column(String)
    # manager refers to an employee id
    manager_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=True)
    location = Column(String, nullable=True)
    # department-level salary multiplier (e.g., engineering 1.15)
    salary_multiplier = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    employees = relationship("Employee", back_populates="department", foreign_keys=lambda: [Employee.department_id])
    positions = relationship("Position", back_populates="department")
