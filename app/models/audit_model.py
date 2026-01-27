from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.database_setup import Base
from datetime import datetime


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(100), nullable=False)  # e.g., "login", "payroll_run", "password_change"
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)
    meta_data = Column(Text, nullable=True)  # JSON string for additional info

    user = relationship("User", back_populates="audit_logs")