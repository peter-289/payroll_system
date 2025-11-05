from backend.database_setups.database_setup import Base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime


class Tax(Base):
    __tablename__ = "tax"

    tax_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    type = Column(String)
    rate = Column(Integer)
    threshold_min = Column(Integer)
    fixed_amount = Column(Integer)
    effective_date = Column(Date, default=datetime.utcnow)
    expiry_date = Column(Date,  default=datetime.utcnow)
    created_at = Column(Date, default=datetime.utcnow)
    updated_at = Column(Date, default=datetime.utcnow, onupdate=datetime.utcnow)

##____RELATIONSHIPS_____
     




