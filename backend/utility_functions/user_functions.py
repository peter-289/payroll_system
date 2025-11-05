from fastapi import Depends,  HTTPException, BackgroundTasks
from backend.database_setups.database_setup import get_db
from backend.dependancies.security import hash_password
from backend.models.roles_model import Role
from backend.models.user_model import User
from sqlalchemy.orm import Session
from backend.dependancies.email_token import create_email_token, verify_email_token
from backend.services.email_service import send_verification_email
from fastapi.background import BackgroundTasks

# ---- User Registration Utility Function ---- #
def register_user(
    background_tasks: BackgroundTasks,
    user_data: dict,
    db: Session
):
    existing_user = db.query(User).filter((User.email == user_data['email']) | (User.username == user_data['username'])).first()
    if existing_user:
        if existing_user.username == user_data['username']:
            raise HTTPException(status_code=400, detail=f"Username {user_data['username']} already taken")
        elif existing_user.email == user_data['email']:
            raise HTTPException(status_code=400, detail=f"Email {user_data['email']} already registered")

    default_role = db.query(Role).filter(Role.role_name == 'employee').first()
    if not default_role:
        raise HTTPException(status_code=500, detail="Default role 'employee' not found. Please contact admin.")
    

    pwd_hash = hash_password(user_data['password'])
    # hash password before storing
    new_user = User(
        name=user_data['name'],
        username=user_data['username'],
        email=user_data['email'],
        password_hash=pwd_hash,
        role_id=default_role.role_id,
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {e}")

    
    # Send email verification link
    try:
        email_token = create_email_token(new_user.user_id, db)
        print(f"Email verification token for {new_user.email}: {email_token}")  # In real app, send this via email
        background_tasks.add_task(send_verification_email, new_user.email, email_token, new_user.name)
        print(f"Email for user :{new_user.email} dispatched successfully!")
    except Exception as e:
        print(f"Failed to send email for user {new_user.email}: {e}")

    # return created user (Pydantic response model will handle conversion)
    return {
        "message": f"User {new_user.username} registered successfully. Check email for more instructions!.",
    }




