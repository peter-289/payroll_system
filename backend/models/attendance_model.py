from backend.database_setups.database_setup import Base
from sqlalchemy import String, Date, Column, Integer, ForeignKey, Float, func, DateTime
from sqlalchemy.orm import relationship


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, default=func.current_date(), nullable=False)
    check_in = Column(DateTime, nullable=True)
    check_out = Column(DateTime, nullable=True)
    status = Column(String, default="present")
    hours_worked = Column(Float, default=0.0)
    overtime_hours = Column(Float, default=0.0)
    remarks = Column(String, nullable=True)


    #----------------------------------------
    #----------Relationships-----------------
    employee = relationship("Employee", back_populates="attendances")