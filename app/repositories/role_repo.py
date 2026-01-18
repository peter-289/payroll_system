from app.models.roles_model import Role
from sqlalchemy.orm import Session
from typing import Optional

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_role_by_id(self, role_id:int)->Optional[Role]:
        return self.db.query(Role).filter(Role.id == role_id).first()
    
    def get_role_by_name(self, rolename: str) -> Optional[Role]:
        return self.db.query(Role).filter(Role.role_name == rolename).first()