from pydantic import BaseModel
from typing import Optional


class PermissionBase(BaseModel):
    permission_name: str
    description: Optional[str] = None


class PermissionCreate(PermissionBase):
    pass


class PermissionResponse(PermissionBase):
    id: int

    model_config = {"from_attributes": True}
