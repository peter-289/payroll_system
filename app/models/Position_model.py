from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, VARCHAR
from app.db.database_setup import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    department_id = Column(Integer, ForeignKey("departments.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))
    #base_salary = Column(Float)
    salary_multiplier = Column(Float, default=1.0)
    #pay_grade = Column(String)
    employment_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

##____Relationships___
    department = relationship("Department", back_populates="positions")
    # employees holding this position (one-to-many)
    employees = relationship("Employee", back_populates="position")
    # single role associated with this position
    role = relationship("Role", back_populates="positions")
    # salaries associated with this position
    salaries = relationship("PositionSalary", back_populates="position")