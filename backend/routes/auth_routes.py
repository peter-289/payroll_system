from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from backend.database_setups.database_setup import get_db
from backend.dependancies.security import get_current_employee, verify_password, hash_password, parse_date, create_login_token
from backend.models.user_model import User
from backend.models.roles_model import Role
from backend.models.employee_model import Employee as Empl
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    prefix="/auth",tags=["Authentication"]
)
#--------------------------------------------------------------------------------------------------
#             --------------- LOGIN ROUTE --------------------
#--------------------------------------------------------------------------------------------------
@router.post("/login", status_code=status.HTTP_200_OK)
def login(
    form_data:OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)):
    username = form_data.username
    password = form_data.password
    """Authenticate user and return a login token."""
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    role = db.query(Role).filter(Role.id == user.role_id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User role not found")
    employee = db.query(Empl).filter(Empl.user_id == user.id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Employee record not found")
    token_data = {
        "sub": str(user.id),
        "employee_id": str(employee.id),
        "role": role.role_name
        }
    access_token = create_login_token(data=token_data)
    if user.must_change_password:
        return{
            "detail":"Password change required!",
            "change required":True, 
            "user_id":user.id
        }    
    return {"access_token": access_token, "token_type": "bearer", "user_id":user.id}



#---------------------------------------------------------------------------------------------------------
#              ------------ CHANGE PASSWORD FOR FIRST TIMERS -----------------
#---------------------------------------------------------------------------------------------------------
@router.post("/change-password", dependencies=[Depends(get_current_employee)])
def change_password(
    user_id:int = Form(...),
    new_password:str = Form(...),
    db:Session = Depends(get_db)
    
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    
    hashed = hash_password(new_password)
    user.password_hash = hashed
    user.must_change_password = False
    db.commit()

    return {"message":"Password changed successfully. You can now login!"}
