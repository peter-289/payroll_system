from app.db.database_setup import Base
from sqlalchemy import String, Date, Column, Integer,Enum, ForeignKey, Float, DateTime, event
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import pytz
from app.domain.enums import AttendanceStatus

EAT = pytz.timezone("Africa/Nairobi")

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    attendance_date = Column(Date, default=func.current_date(), nullable=False)
    check_in = Column(DateTime(timezone=True), nullable=True)
    check_out = Column(DateTime(timezone=True), nullable=True)
    regular_hours = Column(Float, default=0.0)
    hours_worked = Column(Float, default=0.0)
    overtime_hours = Column(Float, default=0.0)
    remarks = Column(String, nullable=True)
    approved = Column(Enum(AttendanceStatus), nullable=True, default=AttendanceStatus.PENDING)


#=======================================================================================================
#---------------------------- RELATIONSHIPS ------------------------------------------------------------
    employee = relationship("Employee", back_populates="attendances")


@event.listens_for(Attendance, 'load')
def receive_load(attendance, *args):
    """Force all loaded datetimes to be EAT-aware"""
    if attendance.check_in and attendance.check_in.tzinfo is None:
        attendance.check_in = EAT.localize(attendance.check_in)
    if attendance.check_out and attendance.check_out.tzinfo is None:
        attendance.check_out = EAT.localize(attendance.check_out)