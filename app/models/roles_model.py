from sqlalchemy import Integer, String, Column
from app.db.database_setup import Base
from sqlalchemy.orm import relationship
from app.models.role_permission import RolePermission

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, default="employee")
    description = Column(String)



    ##__RELATIONSHIPS__
    
    permissions = relationship("Permissions", secondary="role_permissions", back_populates="roles")
    users = relationship("User", back_populates="role")
    positions = relationship("Position", back_populates="role")