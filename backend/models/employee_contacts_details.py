from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.database_setups.database_setup import Base

class EmployeeContact(Base):
    __tablename__ = "employee_contacts"

    contact_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id", ondelete="CASCADE"), unique=True)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=True)
    address = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    
    # one-to-one relationship with employee
    employee = relationship("Employee", back_populates="contact")
