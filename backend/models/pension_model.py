from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Column
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Pension(Base):
    __tablename__ = "pensions"

    pension_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))
    scheme_name = Column(String )
    pension_number = Column(Integer)
    employer_contribution_percentage = Column(Float)
    employee_contribution_percentage = Column(Float)
    monthly_contribution = Column(Integer)
    start_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

##_____RELATIONSHIPS____
    pension = relationship("Eployees", back_populates="employee")


   