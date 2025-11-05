from backend.database_setups.database_setup import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150))
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.role_id'), nullable=True)
    employee_id = Column(Integer, ForeignKey('employees.employee_id', ondelete="CASCADE"), nullable=True)
    status = Column(String, default='inactive')
    last_login = Column(DateTime, default=None)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
   

    # -----Relationships-----
    role = relationship("Role", back_populates="users")
    employee = relationship("Employee", back_populates="user", uselist=False)
    # Relationship with tokens - cascade delete tokens when user is deleted
    tokens = relationship("TokenModel", back_populates="user", cascade="all, delete-orphan")
    # Email verification tokens
   # verification_tokens = relationship("EmailVerificationToken", back_populates="user", cascade="all, delete-orphan")
