from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum, Numeric
from backend.database_setups.database_setup import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class TaxBracket(Base):
    __tablename__ = "tax_brackets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tax_id = Column(Integer, ForeignKey("tax.id"), nullable=False)
    min_amount = Column(Numeric(10, 2), nullable=False)
    max_amount = Column(Numeric(10, 2), nullable=True)
    rate = Column(Numeric(5, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

#==============================================================================================
#____RELATIONSHIPS_____
    tax_rule = relationship("Tax", back_populates="brackets")