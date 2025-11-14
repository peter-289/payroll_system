from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from backend.database_setups.database_setup import get_db
from backend.dependancies.security import check_admin_access, hash_password, parse_date, create_temporary_password
from backend.models.user_model import User

router = APIRouter(
    prefix="/user", tags=["User"]
)

#------------------------------------------------------------------------------------------------------
#----------------------------- CHANGE PASSWORD ----------------------------------------------
