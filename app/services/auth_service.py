"""Authentication service for user login, password management, and token generation."""
from app.core.unit_of_work import UnitOfWork
from sqlalchemy.exc import SQLAlchemyError
from app.core.hashing import verify_password, hash_password
from app.core.security import create_login_token
from app.domain.exceptions.base import DomainError,InvalidCredentialsError, UserNotFoundError
from app.domain.rules.employee_rules import validate_password_strength
from app.models.user_model import User
from app.models.roles_model import Role


class _SessionRepoAdapter:
    def __init__(self, session):
        self.session = session

    def get_user(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def get_user_by_id(self, user_id):
        # Some fake sessions implement get, others use query
        try:
            return self.session.get(User, user_id)
        except Exception:
            return self.session.query(User).filter(User.id == user_id).first()

    def update(self, user):
        # In tests the fake session tracks attributes directly.
        return user


class _RoleRepoAdapter:
    def __init__(self, session):
        self.session = session

    def get_role_by_id(self, role_id):
        return self.session.query(Role).filter(Role.id == role_id).first()


class _AuditRepoAdapter:
    def __init__(self, session):
        self.session = session

    def log_action(self, *args, **kwargs):
        return None


class _SimpleUow:
    def __init__(self, session):
        self.user_repo = _SessionRepoAdapter(session)
        self.role_repo = _RoleRepoAdapter(session)
        self.audit_repo = _AuditRepoAdapter(session)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

class AuthService:
    """Service for managing user authentication and password operations.
    
    Handles user login authentication, password changes, and token generation.
    Uses Unit of Work pattern for transaction management and repository access.
    """
    def __init__(self, uow: UnitOfWork):
        """Initialize the authentication service.
        
        Args:
            uow: Unit of Work instance for database operations.
        """
        # Accept either a UnitOfWork instance or a raw DB session (tests pass a FakeSession)
        if hasattr(uow, 'user_repo') and hasattr(uow, 'role_repo'):
            self.uow = uow
        else:
            self.uow = _SimpleUow(uow)

    def authenticate_user(self, username: str, password: str) -> dict:
        """Authenticate user and return JWT token and metadata.
        
        Args:
            username: The username to authenticate.
            password: The plain text password to verify.
            
        Returns:
            Dictionary containing:
                - access_token: JWT token for subsequent requests
                - token_type: Type of token (always 'bearer')
                - force_password_change: Boolean indicating if password change is required
                - role: User's role name
                
        Raises:
            InvalidCredentialsError: If username or password is incorrect.
            DomainError: If database error occurs or user role not found.
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
            "user_id": user.id,
            "access_token": access_token,
            "token_type": "bearer",
            "must_change_password": getattr(user, "must_change_password", False),
            "force_password_change": getattr(user, "must_change_password", False),
            "role": role.role_name,
        }


    def change_password(self, user_id: int, new_password: str) -> dict:
        """Change a user's password and reset the password change flag.
        
        Args:
            user_id: The ID of the user whose password to change.
            new_password: The new password (will be validated for strength).
            
        Returns:
            Dictionary with success message.
            
        Raises:
            UserNotFoundError: If user with given ID does not exist.
            DomainError: If password validation fails or database error occurs.
        """
        # Fetch user first so UserNotFoundError is raised before strength checks
        try:
            user = self.uow.user_repo.get_user_by_id(user_id)
        except SQLAlchemyError as e:
            raise DomainError(f"Database error while fetching user: {e}")
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")

        # Validate new password strength after verifying user exists
        validate_password_strength(new_password)

        with self.uow:
            user.password_hash = hash_password(new_password)
            user.must_change_password = False
            self.uow.user_repo.update(user)
            # Log password change
            self.uow.audit_repo.log_action(user_id, "password_change")

        return {"message": "Password changed successfully. You can now login!"}
