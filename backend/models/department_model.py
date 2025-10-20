from database import Base
from sqlalchemy import Column, String, Integer, ForeignKey
import datetime
from sqlalchemy.orm import relationship


class Department(Base):
    __tablename__ = "department"

    department_id = Column(Integer,primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True)
    description = Column(String)
    manager_id = Column(Integer, ForeignKey(""))
    location = Column(String)
    created_at = Column(datetime.datetime.utcnow)
    updated_at = Column(datetime.datetime.utcnow)

    #___Relationships
    # Relates to a user
    employees = relationship("Employee", back_populates="department")
