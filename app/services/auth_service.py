from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.user_model import User
from app.models.roles_model import Role
from app.dependancies.security import verify_password, hash_password, create_login_token
from app.exceptions.exceptions import AuthServiceError, InvalidCredentialsError, UserNotFoundError


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(self, username: str, password: str) -> dict:
        """Authenticate user and return token and metadata.
        Raises InvalidCredentialsError for bad creds and AuthServiceError for DB/token errors.
        """
        try:
            user = self.db.query(User).filter(User.username == username).first()
        except SQLAlchemyError as e:
            raise AuthServiceError(f"Database error while fetching user: {e}")

        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError("Invalid username or password")

        try:
            role = self.db.query(Role).filter(Role.id == user.role_id).first()
        except SQLAlchemyError as e:
            raise AuthServiceError(f"Database error while fetching role: {e}")

        if not role:
            raise AuthServiceError("User role not found")

        token_data = {"sub": str(user.id), "role": role.role_name}
        try:
            access_token = create_login_token(data=token_data)
        except Exception as e:
            raise AuthServiceError(f"Failed to create login token: {e}")

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "must_change_password": getattr(user, "must_change_password", False),
        }

    def change_password(self, user_id:int, new_password: str) -> dict:
        """Change a user's password. Raises UserNotFoundError or AuthServiceError on DB errors."""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
        except SQLAlchemyError as e:
            raise AuthServiceError(f"Database error while fetching user: {e}")

        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")

        try:
            user.password_hash = hash_password(new_password)
            user.must_change_password = False
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise AuthServiceError(f"Failed to update password: {e}")

        return {"message": "Password changed successfully. You can now login!"}