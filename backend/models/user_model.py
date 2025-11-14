from backend.database_setups.database_setup import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
import datetime


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(150))
    last_name = Column(String(150))
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=True)
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
    tokens = relationship("TokenModel", back_populates="user", cascade="all, delete-orphan")
   