from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base

class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    gender = Column(String(10), nullable=True)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    hire_date = Column(Date, nullable=False)
    employment_status = Column(String(20), nullable=False)  # e.g., Active, Inactive
    salary_type = Column(Float, nullable=False)
    bank_account_number = Column(String(30), nullable=True)
    bank_name = Column(String(100), nullable=True)
    created_at = Column(Date, nullable=False)
    updated_at = Column(Date, nullable=True)
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    job_role_id = Column(Integer, ForeignKey("job_roles.role_id"))

    # relationships
    department = relationship("Department", back_populates="employees")
    job_role = relationship("JobRole", back_populates="employees")
