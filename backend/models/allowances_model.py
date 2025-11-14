from backend.database_setups.database_setup import Base
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Allowance(Base):
    __tablename__ = "allowances"

    id = Column(Integer, primary_key=True)
    payroll_id = Column(Integer, ForeignKey("payrolls.id"), nullable=False)
    name = Column(Text, nullable=False)
    type = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    payroll = relationship("Payroll", back_populates="allowances")

