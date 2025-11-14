from backend.models.roles_model import Role
from sqlalchemy.orm import Session
from backend.models.user_model import User
from backend.dependancies.security import hash_password, verify_password
from config import ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD


def seed_admin(db:Session):
    try:
        admin = db.query(Role).filter(Role.role_name=='admin').first()
        if not admin:
            admin = Role(role_name='admin', description='System Administrator')
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print('Created admin role id=', admin.id)
        else:
            print('Admin role exists id=', admin.id)
        user = db.query(User).filter(User.username==ADMIN_USERNAME).first()
        if not user:
            user = User(first_name='Administrator', last_name='Peterson', username=ADMIN_USERNAME, password_hash=hash_password(ADMIN_PASSWORD), role_id=admin.id,)
            db.add(user)
            db.commit()
            db.refresh(user)
            print('Created admin user id=', user.id)
        else:
            print('Admin user exists id=', user.id)
        # verify password
        ok = verify_password(ADMIN_PASSWORD, user.password_hash)
        print('Password verify:', ok)
    finally:
        db.close()
