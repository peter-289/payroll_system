from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from app.core.unit_of_work import UnitOfWork
from app.services.auth_service import AuthService
from app.domain.exceptions.base import DomainError, InvalidCredentialsError, UserNotFoundError
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth_schema import LoginResponse
from app.core.security import get_current_employee
from app.db.database_setup import get_db


router = APIRouter(
    prefix="/auth",tags=["Authentication"]
)

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    uow = UnitOfWork(db)
    return AuthService(uow)

#================================================================================================================
#-------------------------- LOGIN ROUTE -------------------------------------------------------------------------
#================================================================================================================
@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(
    form_data:OAuth2PasswordRequestForm = Depends(),
    service:AuthService = Depends(get_auth_service),
):
    username = form_data.username
    password = form_data.password
    """Authenticate user and return a login token."""
    try:
        token_data = service.authenticate_user(username, password)
        return token_data
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

#================================================================================================================
#----------------------- CHANGE PASSWORD ------------------------------------------------------------------------
#================================================================================================================
@router.post("/password")
def change_password(
    new_password:str = Form(...),
    current_employee: dict = Depends(get_current_employee),
    db:Session = Depends(get_db)
    
):
    service = AuthService(UnitOfWork(db))
    try:
        return service.change_password(current_employee["user_id"], new_password)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



