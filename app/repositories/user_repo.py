from app.models.user_model import User
from sqlalchemy.orm import Session
from typing import Optional

class UserRepository:
    def __init__(self, db:Session):
        self.db = db

    def save(self, user:User)-> User:
        self.db.add(user)
        self.db.flush()
        return user
    
    def update(self, user: User) ->User:
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_user(self, username:str)-> Optional[User]:
       return self.db.query(User).filter(User.username == username).first()
    
    def get_user_by_id(self, user_id:int)->Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def delete(self, user: User)->None:
        self.db.delete(user)
        self.db.commit()
