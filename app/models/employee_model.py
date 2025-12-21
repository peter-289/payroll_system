from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.database_setup import Base
from datetime import datetime
from datetime import date
from enum import Enum
from sqlalchemy import Enum as SqlEnum


class SalaryTypeEnum(str, Enum):
    MONTHLY = "monthly"
    HOURLY = "hourly"
    CONTRACT = "contract"

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=True)
    hire_date = Column(Date, nullable=False, default=date.today)
    salary_type = Column(SqlEnum(SalaryTypeEnum, name="salary_type_enum", native_enum=True), default=SalaryTypeEnum.MONTHLY)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    approval_status = Column(String(20), default="pending")



# -----------------------------------------------------------------------------------------------------
#----------------------------- RELATIONSHIPS ----------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
    user = relationship("User", back_populates="employee", uselist=False)
    department = relationship("Department", back_populates="employees", foreign_keys=[department_id])
    position = relationship("Position", back_populates="employees", foreign_keys=[position_id], uselist=False)
    insurances = relationship("Insurance", back_populates="employee", cascade="all, delete-orphan")
    loans = relationship("Loan", back_populates="employee", cascade="all, delete-orphan")
    pensions = relationship("Pension", back_populates="employee", cascade="all, delete-orphan")
    payrolls = relationship("Payroll", back_populates="employee", cascade="all, delete-orphan")
    bank_accounts = relationship("EmployeeBankAccount", back_populates="employee", cascade="all, delete-orphan")
    contact = relationship("EmployeeContact", back_populates="employee", uselist=False, cascade="all, delete-orphan")
    attendances = relationship("Attendance", back_populates="employee", cascade="all, delete")
    # salaries: historical and current employee-specific salary records
    salaries = relationship("EmployeeSalary", back_populates="employee", cascade="all, delete-orphan")