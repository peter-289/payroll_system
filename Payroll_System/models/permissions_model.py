from sqlalchemy import Integer, String, Column
from database import Base

class Permissions(Base):
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, index=True)
    permisson_name = Column(String)
    description = Column(String)

    ##___Relationships___
    