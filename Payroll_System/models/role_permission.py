from database import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Role_Permission(Base):
    __tablename__ = "role_permission"

    role_id = Column (Integer, ForeignKey("role.role_id"), primary_key=True, index=True)
    permission_id = Column(Integer, ForeignKey("permission.permission_id"))

    ##____RELATIONSHIPS____
    role_permission = relationship("Roles", back_populates="role")
    role_permission = relationship("Permission", back_populates="permission")

