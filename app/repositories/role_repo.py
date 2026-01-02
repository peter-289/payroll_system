from app.models.roles_model import Role
from sqlalchemy.orm import Session

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_role(self, role_id:int)-> Role:
        return self.db.query(Role).filter(Role.id == role_id).first()
    
    