from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, VARCHAR
from database import Base
from datetime import datetime


class Position(Base):
    __tablename__ = "position"

    role_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    department_id = Column(Integer, ForeignKey("department.department_id"))
    base_salary = Column(Float)
    pay_grade = Column(VARCHAR)
    employment_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

##____Relationships___
