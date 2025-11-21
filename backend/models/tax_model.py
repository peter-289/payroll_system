from backend.database_setups.database_setup import Base
from sqlalchemy import Column, Integer, String, DateTime, Enum, Numeric
from datetime import datetime
import enum
from sqlalchemy.orm import relationship


class TaxType(enum.Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"
    TIERED = "tiered"

class Tax(Base):
    __tablename__ = "tax"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    type = Column(Enum(TaxType), nullable=False, default=TaxType.PERCENTAGE)
    #fixed_amount = Column((Numeric(10, 2)), nullable=True)
    effective_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime,  nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

##____RELATIONSHIPS_____
    brackets = relationship("TaxBracket", back_populates="tax_rule", cascade="all, delete-orphan")




