from backend.models import user_model, role_permission, roles_model, permissions_model, payroll_model, deductions_model, allowances_model, Loans_advances_model, pension_model, Insuarance_model, tax_model, department_model, Position_model, employee_model, employee_contacts_details, employee_bank_account, token_model, attendance_model, tax_brackets
from asyncio.log import logger
from backend.database_setups.database_setup import Base, engine


def init_db():
    """Create database tables based on SQLAlchemy models."""
    try:
      Base.metadata.create_all(bind=engine)
      #Base.metadata.drop_all(bind=engine)
    except Exception as e:
       logger.exception(f"Failed to create database tables: {e}")
       # Optionally, you can drop all tables if needed