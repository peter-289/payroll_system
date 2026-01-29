"""User model representing system users and their authentication information."""
from app.db.database_setup import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Date
from sqlalchemy.orm import relationship
import datetime



class User(Base):
    """User account model for system authentication and authorization.
    
    Attributes:
        id: Unique identifier for the user.
        role_id: Foreign key reference to the user's role.
        first_name: User's first name.
        last_name: User's last name.
        username: Unique username for login (required).
        gender: User's gender.
        date_of_birth: User's date of birth.
        password_hash: Hashed password for authentication.
        status: Account status (active/inactive).
        last_login: Timestamp of last login.
        created_at: Timestamp when user account was created.
        updated_at: Timestamp of last account update.
        must_change_password: Boolean flag indicating if password change is required.
    
    Relationships:
        role: Associated Role object.
        employee: Associated Employee object (one-to-one).
        position_salaries: Associated PositionSalary records.
        employee_salaries: Associated EmployeeSalary records.
        audit_logs: Associated AuditLog records.
    """
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
    audit_logs = relationship("AuditLog", back_populates="user")