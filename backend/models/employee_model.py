from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from backend.database_setups.database_setup import Base
from datetime import datetime

from backend.models.employee_bank_account import EmployeeBankAccount
from backend.models.employee_contacts_details import EmployeeContact
from datetime import date

class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    gender = Column(String(10), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    hire_date = Column(Date, nullable=False, default=date.today())
    employment_status = Column(String(20), nullable=False, default="Pending")  # e.g., Active, Inactive
    salary_type = Column(String, nullable=False, )
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    position_id = Column(Integer, ForeignKey("positions.position_id"), nullable=True)
    approval_status = Column(String(20), default="pending")  # e.g., pending, approved, rejected




    # relationships
    department = relationship("Department", back_populates="employees", foreign_keys=[department_id])
    # position relationship (each employee has one current position)
    position = relationship("Position", back_populates="employees", foreign_keys=[position_id], uselist=False)
    # link to user account (if any)
    user = relationship("User", back_populates="employee", uselist=False)

    # insurances and other related records
    insurances = relationship("Insurance", back_populates="employee", cascade="all, delete-orphan")
    loans = relationship("Loan", back_populates="employee", cascade="all, delete-orphan")
    pensions = relationship("Pension", back_populates="employee", cascade="all, delete-orphan")
    payrolls = relationship("Payroll", back_populates="employee", cascade="all, delete-orphan")

    # one-to-many relationship with bank accounts
    bank_accounts = relationship("EmployeeBankAccount", back_populates="employee", cascade="all, delete-orphan")

    # one-to-one relationship with contact details
    contact = relationship("EmployeeContact", back_populates="employee", uselist=False, cascade="all, delete-orphan")
