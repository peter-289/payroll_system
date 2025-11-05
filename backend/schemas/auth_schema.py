from pydantic import BaseModel
from typing import Optional

class TokenData(BaseModel):
    username: str
    exp: Optional[int] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str
    role: str