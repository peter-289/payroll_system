"""Security helpers for authentication, authorization and password management."""

from datetime import date, datetime, timedelta
from typing import Optional, List
import hashlib
import os
import binascii
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.models.user_model import User
from pydantic import BaseModel
from app.models.employee_model import Employee
from sqlalchemy.orm import Session
from app.db.database_setup import get_db
from app.config import LOGIN_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class Token(BaseModel):
    access_token: str
    token_type: str

#======================================================================================================
#------------------------ TOKEN DATA ---------------------------------------------------------------
class TokenData(BaseModel):
    username: Optional[str] = None
    permissions: List[str] = []

def hash_password(password: str) -> str:
    """Hash password with PBKDF2-HMAC-SHA256; return salt+hash hex string."""
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
    return binascii.hexlify(salt).decode() + ':' + binascii.hexlify(dk).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the hashed password using PBKDF2."""
    try:
        salt_hex, dk_hex = hashed_password.split(':')
        salt = binascii.unhexlify(salt_hex)
        expected = binascii.unhexlify(dk_hex)
        dk = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, 100_000)
        if len(dk) != len(expected):
            return False
        result = 0
        for a, b in zip(dk, expected):
            result |= a ^ b
        return result == 0
    except Exception:
        return False
    


#======================================================================================================
#------------------------ CREATE A LOGIN TOKEN TO MANAGE SESSIONS -------------------------------------
def create_login_token(data:dict, expires_delta:timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=LOGIN_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})
    token = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)
    return token



#======================================================================================================
#------------------------ DECODE TOKEN ---------------------------------------------------------------
def get_current_employee(
    token: str = Depends(oauth2_scheme)
):
    """Get the current authenticated employee from the JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception

    return {
         "user_id": user_id,"role":role
    }



#======================================================================================================
#------------------------ GET CURRENT ACTIVE USER ---------------------------------------------------


#======================================================================================================
#------------------------ CHECK ADMIN ACCESS -------------------------------------------------------
def admin_access(
    current_employee: dict = Depends(get_current_employee)
):
    if current_employee.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_employee


#======================================================================================================
#------------------------ CHECK HR ACCESS -------------------------------------------------------------
def hr_access(
    current_employee: dict = Depends(get_current_employee)
):
    if current_employee.get("role") != "hr":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="HR access required"
        )
    return current_employee


def admin_hr_or_self(
    current_employee: dict = Depends(get_current_employee)
):
    """Allow access if current user is admin, hr, or the employee themself."""
    role = current_employee.get("role")
    if role in ("admin", "hr", "employee"):
        return current_employee
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Admin/HR or owner access required"
    )


#======================================================================================================
#------------------------ PARSE DATE FROM DIFFERENT FORMATS ---------------------------------------------
def parse_date(value):
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
def create_temporary_password(length:int = 12) -> str:
    """Generate a random temporary password of specified length."""
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()"
    password = ''.join(
        characters[os.urandom(1)[0] % len(characters)]
        for _ in range(length)
    )
    return password