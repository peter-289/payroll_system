from app.core.unit_of_work import UnitOfWork
from sqlalchemy.exc import SQLAlchemyError
from app.core.hashing import verify_password, hash_password
from app.core.security import create_login_token
from app.domain.exceptions.base import DomainError,InvalidCredentialsError, UserNotFoundError
from app.domain.rules.employee_rules import validate_password_strength

class AuthService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def authenticate_user(self, username: str, password: str) -> dict:
        """Authenticate user and return token and metadata.
        Raises InvalidCredentialsError for bad creds and DomainError for DB/token errors.
        """
        try:
            user = self.uow.user_repo.get_user(username)
            if not user or not verify_password(user.password_hash, password):
               raise InvalidCredentialsError("Invalid username or password")
            
            role = self.uow.role_repo.get_role_by_id(user.role_id)
            if not role:
               raise DomainError("User role not found")
            
            token_data = {
                "sub": str(user.id), 
                "role": role.role_name
                }
            access_token = create_login_token(data=token_data)

        except SQLAlchemyError as e:
            raise DomainError(f"Database error: {e}")
        
        

        

        # Log login
        self.uow.audit_repo.log_action(user.id, "login", {"role": role.role_name})

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "force_password_change": getattr(user, "must_change_password", False),
            "role":role.role_name,
        }


    def change_password(self, user_id:int, new_password: str) -> dict:
        """Change a user's password. Raises UserNotFoundError or DomainError on DB errors."""
        # Validate new password strength
        validate_password_strength(new_password)
       
        try:
            user = self.uow.user_repo.get_user_by_id(user_id)
        except SQLAlchemyError as e:
            raise DomainError(f"Database error while fetching user: {e}")

        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")

        with self.uow:
            user.password_hash = hash_password(new_password)
            user.must_change_password = False
            self.uow.user_repo.update(user)
            # Log password change
            self.uow.audit_repo.log_action(user_id, "password_change")

        return {"message": "Password changed successfully. You can now login!"}
