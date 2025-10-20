from sqlalchemy import Integer, String, Column
from database import Base
from sqlalchemy.orm import relationship

class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String)
    description = Column(String)

    ##__RELATIONSHIPS__