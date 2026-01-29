"""Security helpers for authentication, authorization and password management."""
from datetime import date, datetime, timedelta
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import LOGIN_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from app.repositories.employee_repo import EmployeeRepository
from sqlalchemy.orm import Session
from app.db.database_setup import get_db
from app.domain.exceptions.base import ValidationError
from app.core.hashing import hash_password, verify_password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Credentials exception for invalid tokens
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)




#======================================================================================================
#------------------------ CREATE A LOGIN TOKEN TO MANAGE SESSIONS -------------------------------------
def create_login_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT login token with encoded data and expiration time.
    
    Args:
        data: Dictionary containing token payload (should include 'sub' for user_id and 'role').
        expires_delta: Optional custom expiration time. If None, uses LOGIN_TOKEN_EXPIRE_MINUTES.
        
    Returns:
        Encoded JWT token string.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=LOGIN_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

#=====================================================================================================
#------------------------ GET CURRENT USER -----------------------------------------------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> dict:
    """Decode JWT token and return current user information.
    
    Args:
        token: JWT bearer token from request header.
        
    Returns:
        Dictionary containing user_id and role.
        
    Raises:
        HTTPException: If token is invalid or credentials cannot be validated.
    """
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        role: str = payload.get("role")
        
        if user_id is None or role is None:
            raise credentials_exception
     
    except JWTError:
        raise credentials_exception

    return {
         "user_id": user_id, 
         "role":role
    }

#======================================================================================================
#------------------------ GET CURRENT EMPLOYEE ---------------------------------------------------------------
def get_current_employee(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> dict:
    """Decode JWT token and return current employee information.
    
    Args:
        token: JWT bearer token from request header.
        db: SQLAlchemy database session.
        
    Returns:
        Dictionary containing user_id, employee_id, and role.
        
    Raises:
        HTTPException: If token is invalid or employee record not found.
        ValidationError: If employee cannot be retrieved for the user.
    """
    employee_repo = EmployeeRepository(db)
    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        role: str = payload.get("role")
        
        employee = employee_repo.get_by_user_id(user_id)
        if employee is None:
            raise ValidationError("Failed to get employee for current user")
    except JWTError:
        raise credentials_exception

    return {
         "user_id": user_id,
         "employee_id":employee.id, 
         "role":role
    }


#======================================================================================================
#------------------------ CHECK ADMIN ACCESS -------------------------------------------------------
def admin_access(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """Verify that the current user has admin role access.
    
    Args:
        current_user: Current user dictionary from get_current_user dependency.
        
    Returns:
        The current user dictionary if authorized.
        
    Raises:
        HTTPException: If user does not have admin role.
    """

    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


#======================================================================================================
#------------------------ CHECK HR ACCESS -------------------------------------------------------------
def hr_access(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """Verify that the current user has HR role access.
    
    Args:
        current_user: Current user dictionary from get_current_user dependency.
        
    Returns:
        The current user dictionary if authorized.
        
    Raises:
        HTTPException: If user does not have HR role.
    """
    if current_user.get("role") != "hr":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="HR access required"
        )
    return current_user


def admin_hr_or_self(
    current_user: dict = Depends(get_current_employee)
) -> dict:
    """Verify access for admin, HR, or the employee accessing their own record.
    
    Args:
        current_user: Current employee dictionary from get_current_employee dependency.
        
    Returns:
        The current user dictionary if authorized.
        
    Raises:
        HTTPException: If user does not have admin/hr role or is not the employee owner.
    """
    role = current_user.get("role")
    if role in ("admin", "hr", "employee"):
        return current_user
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Admin/HR or owner access required"
    )


#======================================================================================================
#------------------------ PARSE DATE FROM DIFFERENT FORMATS ---------------------------------------------
def parse_date(value) -> date:
    """Parse date from multiple common formats.
    
    Args:
        value: Date value as date object or string in various formats.
        
    Returns:
        Parsed date object.
        
    Raises:
        HTTPException: If date format is not recognized.
    """
    if isinstance(value, date):
        return value
    elif isinstance(value, str):
        raw = value.strip()

    patterns = [
        "%Y-%m-%d",   # 2000-01-31  ← ISO (recommended)
        "%d/%m/%Y",   # 31/01/2000  ← Europe
        "%m/%d/%Y",   # 01/31/2000  ← USA
        "%d-%m-%Y",   # 31-01-2000
        "%Y/%m/%d",   # 2000/01/31
        "%b %d, %Y",  # Jan 31, 2000
        "%d %b %Y",   # 31 Jan 2000
    ]

    for format in patterns:
        try:
            return datetime.strptime(raw, format).date()
        except ValueError:
            continue
    
    raise HTTPException(
        status_code=400,
        detail=(
            "Invalid date. "
            "Use one of: YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY, "
            "DD-MM-YYYY, YYYY/MM/DD, 'Jan 31, 2000' or '31 Jan 2000'"
        )
    )


#------------------------------------------------------------------------------------------------
#           ----- CREATE TEMPORARY PASSWORD ------
#------------------------------------------------------------------------------------------------
def create_temporary_password(length: int = 12) -> str:
    """Generate a random temporary password of specified length.
    
    Args:
        length: Desired password length (default 12).
        
    Returns:
        Random password string containing uppercase, lowercase, digits, and special characters.
    """
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()"
    password = ''.join(
        characters[os.urandom(1)[0] % len(characters)]
        for _ in range(length)
    )
    return password