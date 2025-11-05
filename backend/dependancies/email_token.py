from datetime import datetime, timedelta
from backend.models.token_model import TokenModel
import jwt
from config import SECRET_KEY, ALGORITHM, EMAIL_TOKEN_EXPIRE_MINUTES
from fastapi import HTTPException
from sqlalchemy.orm import Session
from jwt import InvalidTokenError, ExpiredSignatureError




def create_email_token(user_id: int, db:Session, token_type: str = 'email_verification') -> str:
    expire = datetime.utcnow() + timedelta(minutes=EMAIL_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "type": token_type,
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    user_token = TokenModel(
        token=token,
        token_type=token_type,
        user_id=user_id,
        expires_at=expire,
        is_used = False

    )
    
    db.add(user_token)
    db.commit()
    db.refresh(user_token)
    print(f"Token saved to DB: {user_token.token}")


    return token




def verify_email_token(token: str, db:Session, expected_type: str = 'email_verification') -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        user_id_str = payload.get("sub")
        token_type = payload.get("type")
        print(f"{user_id_str}, {token_type}")

        if user_id_str is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        if token_type != expected_type:
            raise HTTPException(status_code=401, detail="Invalid token type")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired token")
    except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

    
    user_id = int(user_id_str)

    return {"user_id": user_id, "token_type": token_type, "message": "Token for verification is valid"}



#-----------------------------------------------------------------------------
#   CREATE A TEMPORARY TOKEN FOR EMPLOYEE REGISTRATION
# ----------------------------------------------------------------------------

def create_temp_token(user_id:int, db, token_type = "employee registration")->str:
    REG_EXPIRE_MINUTES = 30
    expire = datetime.utcnow() + timedelta(minutes=REG_EXPIRE_MINUTES)
    payload = {
      "sub":str(user_id),       
      "type":token_type,
      "exp":expire
    }
    
    token =jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    new_token = TokenModel(
        token = token,
        token_type = token_type,
        user_id = user_id,
        expires_at = expire,
        is_used = False

    )
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    print(f"Temp token saved to db:{token}")

    return token


#--------------------------------------------------------------------------------------
# ------- DECODE THE TEMPORARY TOKEN --------------------------------------------------
#--------------------------------------------------------------------------------------
def decode_temp_token(token:str, db, expected_type = "employee registration") -> dict:

    try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired!")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token!")
   
   
   
    user_id_str = payload.get("sub")
    token_type = payload.get("type")
    
    

    if token_type != expected_type:
        raise HTTPException(status_code=401, detail="Invalid token type!")
    
    if not user_id_str:
        raise HTTPException(status_code=401, detail="Invalid token no id!")
    
    token_record = db.query(TokenModel).filter(TokenModel.token == token, TokenModel.is_used == False).first()
    if not token_record:
        raise HTTPException(status_code=401, detail="Token not found!")
    
    user_id = int(user_id_str)

    return {"message":"Token is valid for verification!","user_id":user_id, "token_type":token_type}
