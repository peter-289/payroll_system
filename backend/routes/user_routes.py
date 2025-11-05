"""Routes for regular user operations."""

from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException, Request
from sqlalchemy.orm import Session
from backend.database_setups.database_setup import get_db
from backend.models.user_model import User
from backend.models.role_permission import RolePermission
from backend.models.roles_model import Role
from backend.models.employee_model import Employee
from backend.models.employee_bank_account import EmployeeBankAccount
from backend.models.employee_contacts_details import EmployeeContact
from backend.schemas.user_schema import UserResponse
from backend.schemas.role_permission_schema import RolePermissionResponse
from backend.utility_functions.user_functions import register_user
from backend.dependancies.email_token import create_email_token, decode_temp_token
from backend.services.email_service import send_verification_email
from sqlalchemy.exc import SQLAlchemyError
from datetime import date
from fastapi.responses import JSONResponse, HTMLResponse
from backend.models.department_model import Department
from backend.models.Position_model import Position
from backend.models.token_model import TokenModel
from backend.dependancies.security import parse_date
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/api", tags=["User Operations"])
templates = Jinja2Templates(directory="backend/templates")



# ---- User Registration ---- #
@router.post("/register")
def register(
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    
    user_data = {
        "name": name,
        "username": username,
        "email": email,
        "password": password
    }
      # Placeholder, replace with actual BackgroundTasks if needed
    try:
        result = register_user(background_tasks, user_data, db)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    return result



# ----Get user with username ----
@router.get("/users/{username}", response_model=UserResponse)
def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ----Employee Registration----#




# ---- Test role_permission relationship ----
@router.get('/my-role-permissions', response_model=list[RolePermissionResponse])
def get_my_role_permissions(
    db: Session = Depends(get_db),
    
):
    role = db.query(RolePermission).all()
    
    return role

# ---- Test Role-Permissions----#
@router.get("/role-names")
def get_role_name(db:Session = Depends(get_db)):
    role_names = db.query(Role.role_name).all()
    if not role_names:
        raise HTTPException(status_code=404, detail="No roles found")
    roles_names = [r[0] for r in role_names]
    return roles_names
    

# -----Employee registration-----
@router.post("/employee-registration/submit", response_class=HTMLResponse, response_model=None)
def employee_registration(
    request:Request,
    token:str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    gender: str = Form(...),
    date_of_birth: str= Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
    city: str = Form(...),
    country: str = Form(...),
    bank_name: str = Form(...),
    account_number: str = Form(...),
    account_type: str = Form(...),
    position_name: str = Form(...),
    department_name: str = Form(...),
    db: Session = Depends(get_db)
):
    #return {"message":"form parsed successfullyy!"}

    token_data = decode_temp_token(token, db)
    user_id = token_data['user_id']
    
    user_record = db.query(User).filter(User.user_id == user_id, User.status == "active").first()
    if not user_record:
        raise HTTPException(status_code=401, detail= " User is not verified!")
    
    try:
        dob = parse_date(date_of_birth)
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid date format")
    
    department = db.query(Department).filter(Department.name == department_name).first()
    if not department:
        raise HTTPException(status_code=404, detail=f"Department: {department_name} does not exist!")
    
    position = db.query(Position).filter(Position.title == position_name).first()
    if not position:
        raise HTTPException(status_code=404, detail=f"Position: {position_name} does not exist!")


    new_employee = Employee(
        first_name = first_name,
        last_name = last_name,
        gender =gender,
        date_of_birth = dob,
        hire_date = date.today(),
        salary_type = "monthly",
        department_id = department.department_id,
        position_id = position.position_id

    )
    
    
    token_record = db.query(TokenModel).filter(TokenModel.token == token, TokenModel.is_used == False).first()
    try:
        db.add(new_employee)
        db.flush()
        db.refresh(new_employee)
        contact_details = EmployeeContact(
          employee_id = new_employee.employee_id,
          email = email,
          phone = phone,
          address = address,
          city = city,
         country = country
        )    
        
        
    
        bank_details = EmployeeBankAccount(
           employee_id = new_employee.employee_id,
           bank_name = bank_name,
           account_number = account_number,
           account_type = account_type
        )    

        db.add(contact_details)
        db.add(bank_details)

        token_record.is_used = True
        user_record.status = "employed"
        user_record.employee_id = new_employee.employee_id
        
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"DB error {e}")
    
    return templates.TemplateResponse(
        "employee_registration_success.html",
        {"request":request, "name":user_record.name}

    )

    