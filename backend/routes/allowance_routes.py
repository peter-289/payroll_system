from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database_setups.database_setup import get_db

router = APIRouter(
    prefix="/allowances",tags=["Allowances"]
)