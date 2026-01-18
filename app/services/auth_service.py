from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.hashing import verify_password, hash_password
from app.core.security import create_login_token
from app.domain.exceptions.base import AuthServiceError, InvalidCredentialsError, UserNotFoundError
from app.repositories.user_repo import UserRepository
from app.repositories.role_repo import RoleRepository

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository
        self.role_repo = RoleRepository

    def authenticate_user(self, username: str, password: str) -> dict:
        """Authenticate user and return token and metadata.
        Raises InvalidCredentialsError for bad creds and AuthServiceError for DB/token errors.
        """
        try:
            user = self.user_repo.get_user(self, username)
        except SQLAlchemyError as e:
            raise AuthServiceError(f"Database error while fetching user: {e}")

        if not user or not verify_password(user.password_hash, password):
            raise InvalidCredentialsError("Invalid username or password")
        try:
            role = self.role_repo.get_role(self, user.role_id)
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
            "username":user.username,
            "role":role.role_name,
            "must_change_password": getattr(user, "must_change_password", False),
        }


    def change_password(self, user_id:int, new_password: str) -> dict:
        """Change a user's password. Raises UserNotFoundError or AuthServiceError on DB errors."""
        try:
            user = self.user_repo.get_user_by_id(user_id)
        except SQLAlchemyError as e:
            raise AuthServiceError(f"Database error while fetching user: {e}")

        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")

        try:
            user.password_hash = hash_password(new_password)
            user.must_change_password = False
            self.user_repo.update(user)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise AuthServiceError(f"Failed to update password: {e}")

        return {"message": "Password changed successfully. You can now login!"}