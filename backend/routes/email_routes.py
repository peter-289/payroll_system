from fastapi import APIRouter, Depends, Form, HTTPException, Request
from sqlalchemy.orm import Session
from backend.database_setups.database_setup import get_db
from backend.models.user_model import User
from backend.dependancies.email_token import  verify_email_token, create_temp_token,decode_temp_token
from fastapi.responses import  HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.models.department_model import Department
from backend.models.Position_model import Position

from backend.models.token_model import TokenModel
from backend.models.roles_model import Role



router = APIRouter(prefix="/api", tags=["Email Operations"])
templates = Jinja2Templates(directory="backend/templates")



@router.get("/email/verify", response_class=HTMLResponse)
def verify_email_token_route(request: Request, token: str, db: Session = Depends(get_db)):
    """Route to verify email using token."""
    token_data = verify_email_token(token, db)
    print(f"Token data verified: {token_data}")
    user = db.query(User).filter(User.user_id == token_data["user_id"]).first()
    if not user:
        return templates.TemplateResponse("email_verification_error.html", {"request": request, "detail": "User not found."})
    if user.status == 'active':
        return templates.TemplateResponse("email_already_verified.html", {"request": request, "detail": "User already verified."})

    token_db = db.query(TokenModel).filter(TokenModel.token == token, TokenModel.is_used == False).first()
    if not token_db:
          return templates.TemplateResponse("email_verification_error.html", {"request": request, "detail": "Token not found or already used."})
    if token_db.is_used == True:
          return templates.TemplateResponse("email_already_verified.html", {"request": request, "detail": "Token has already been used."})
    #reg_token = db.query(TokenModel).filter(TokenModel.token_type == "employee registration", TokenModel.is_used == False).first()
    reg_token = create_temp_token(user.user_id, db)
    url = f"/api/employee-registration/verify?token={reg_token}"

    user.status = 'active'
    db.commit()
     
    token_db.is_used = True
    db.commit()
    print(f"rendering template for user: {user.name}")
    return templates.TemplateResponse(
         "success_email_verification.html",
           {"request": request,
             "name": user.name,
             "registration_url":url
             })

   
    

@router.get("/employee-registration/verify", response_class=HTMLResponse)
def employee_registration(request: Request, token:str, db: Session = Depends(get_db)):
    """Route to verify employee registration."""
    try:
       token_data = decode_temp_token(token, db)
    except HTTPException:
       return templates.TemplateResponse(
           "error.html",
           {"request":request, "detail":"Invalid or expired registration link!"}
       )
    
    user_id = token_data["user_id"]
           
    user_record = db.query(User).join(TokenModel, User.user_id == TokenModel.user_id).filter(User.user_id == user_id, TokenModel.is_used == False).first()

    if not user_record:
         return templates.TemplateResponse(
             "error.html",
             {"request":request, "detail":"No active registration Sessions"}
         )
    
    token_record = db.query(TokenModel).filter(TokenModel.user_id == user_id, TokenModel.is_used == False).first()
    if not token_record:
         return templates.TemplateResponse(
             "error.html",
             {"request":request, "detail":"Registration token already used!"}
         )
    
    
    departments = db.query(Department).all()
    positions = db.query(Position).all()

    _token = token
    return templates.TemplateResponse(
         "employee_registration.html",
           {"request": request,
            "departments":departments, 
            "positions": positions, 
            "user": user_record, 
            "token":_token,
            "detail": "Employee registration verification."})
