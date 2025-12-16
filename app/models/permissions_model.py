from sqlalchemy import Integer, String, Column
from app.db.database_setup import Base
from sqlalchemy.orm import relationship
from app.models.role_permission import RolePermission

class Permissions(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    permission_name = Column(String)
    description = Column(String)

    ##___Relationships___
    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")
    
    