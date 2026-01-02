from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from app.db.database_setup import get_db
from app.services.auth_service import AuthService
from app.exceptions.exceptions import AuthServiceError, InvalidCredentialsError, UserNotFoundError
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth_schema import LoginResponse


router = APIRouter(
    prefix="/auth",tags=["Authentication"]
)
#================================================================================================================
#-------------------------- LOGIN ROUTE -------------------------------------------------------------------------
#================================================================================================================
@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(
    form_data:OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)):
    username = form_data.username
    password = form_data.password
    """Authenticate user and return a login token."""
    service = AuthService(db)
    try:
        token_data = service.authenticate_user(username, password)
        return token_data
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except AuthServiceError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

#================================================================================================================
#----------------------- CHANGE PASSWORD ------------------------------------------------------------------------
#================================================================================================================
@router.post("/password")
def change_password(
    user_id:str = Form(...),
    new_password:str = Form(...),
    db:Session = Depends(get_db)
    
):
    service = AuthService(db)
    try:
        return service.change_password(user_id, new_password)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AuthServiceError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



