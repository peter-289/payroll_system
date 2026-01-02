from fastapi import Depends
from app.models.roles_model import Role
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.core.hashing import hash_password, verify_password
from app.core.config import ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD
from app.db.database_setup import get_db


def seed_admin(db:Session = Depends(get_db)):
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
            user = User(
                role_id=admin.id,
                first_name='Administrator',
                last_name='hinsei',
                username=ADMIN_USERNAME,
                gender='Not Specified',
                date_of_birth=None,
                password_hash=hash_password(ADMIN_PASSWORD),
                status='active',
                must_change_password=False)
            db.add(user)
            db.commit()
            db.refresh(user)
            print('Created admin user id:', user.id)
        else:
            print('Admin user exists id:', user.id)
        # verify password
        ok = verify_password(user.password_hash, ADMIN_PASSWORD)
        print('Password verify:', ok)
    except Exception as e:
        print('Error seeding admin user:', e)
