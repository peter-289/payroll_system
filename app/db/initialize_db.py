from app.models import user_model,insurance_model, role_permission, roles_model, permissions_model, payroll_model, deductions_model, allowances_model, Loans_advances_model, pension_model, tax_model, department_model, salary_model, Position_model, employee_model, employee_contacts_details, employee_bank_account, attendance_model, tax_brackets, audit_model
from asyncio.log import logger
from app.db.database_setup import Base, engine



def init_db():
    """Create database tables based on SQLAlchemy models."""
    try:
      Base.metadata.create_all(bind=engine)
      #Base.metadata.drop_all(bind=engine)
    except Exception as e:
       logger.exception(f"Failed to create database tables: {e}")
       