from app.db.database_setup import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Date
from sqlalchemy.orm import relationship
import datetime



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=True)
    first_name = Column(String(150))
    last_name = Column(String(150))
    username = Column(String, unique=True, index=True, nullable=False)
    gender = Column(String(10), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    password_hash = Column(String, nullable=False)
    status = Column(String, default='inactive')
    last_login = Column(DateTime, default=None)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    must_change_password = Column(Boolean, default=True)

#-----------------------------------------------------------------------------------------------------  
#----------------------------- RELATIONSHIPS ----------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
    role = relationship("Role", back_populates="users")
    employee = relationship("Employee", back_populates="user", uselist=False)
    position_salaries = relationship("PositionSalary", back_populates="user")
    employee_salaries = relationship("EmployeeSalary", back_populates="user")