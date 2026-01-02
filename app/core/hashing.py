from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError
import unicodedata
from typing import Optional


ph = PasswordHasher(
    time_cost=3,
    memory_cost=102400,
    parallelism=4
)



def _normalize_password(password:str)->str:
    """
    Normalize password
    params password: str
    """
    return unicodedata.normalize("NFKC", password)


def hash_password(password:str):
    """
    Hash password:
    params password: str
    """
    password = _normalize_password(password)
    hashed = ph.hash(password)
    return hashed


def verify_password(stored_hash:str, password:str)-> Optional[str]:
    """
    Verify password 
    params stored_hash: str, password: str

    """
    password = _normalize_password(password)
    try:
        ph.verify(stored_hash, password)
    except VerifyMismatchError:
        return None
    except InvalidHashError:
        raise RuntimeError("Stored password hash is invalid!")
    if ph.check_needs_rehash(stored_hash):
        return ph.hash(password)
    return stored_hash





