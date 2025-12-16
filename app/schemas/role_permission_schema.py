from pydantic import BaseModel
from typing import Optional


class RolePermissionBase(BaseModel):
    role_id: int
    permission_id: int


class RolePermissionCreate(RolePermissionBase):
    pass


class RolePermissionResponse(RolePermissionBase):
    role_id: int
    permission_id: int

    class Config:
       from_attributes = True
       