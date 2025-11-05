"""Security helpers for authentication, authorization and password management."""

from datetime import datetime, timedelta
from typing import Optional, List
import hashlib
import os
import binascii
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from backend.database_setups.database_setup import get_db
from backend.models.user_model import User
from pydantic import BaseModel

# Security configuration
SECRET_KEY = "YOUR-SECRET-KEY-HERE"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

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

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a new JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user from the JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get the current active user, checking if they're not disabled."""
    if current_user.status != "active":
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def check_admin_access(current_user: User = Depends(get_current_active_user)) -> User:
    """Check if the current user has admin privileges."""
    if not current_user.role or current_user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

#------------------------------------------------------------------------------------------------
#           ----- PARSE DATE ------
#------------------------------------------------------------------------------------------------

def parse_date(date:str):
    raw = date.strip()

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