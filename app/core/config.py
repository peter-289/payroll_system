"""Configuration module for the payroll system application.

This module handles all application configuration including database connection,
security settings, and authentication parameters loaded from environment variables.
All values default to safe development settings if environment variables are not set.
"""
import os
from pathlib import Path
#from fastapi_mail import ConnectionConfig
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # dotenv not available — rely on environment variables or defaults
    pass



# Default to a local SQLite file if DATABASE_URL not provided
DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///./payroll.db"
SECRET_KEY = os.getenv("SECRET_KEY") or "dev-secret-change-me"
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME") or "admin"
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL") or "admin@example.com"
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD") or "AdminPass123!"
EMAIL_TOKEN_EXPIRE_MINUTES = int(os.getenv("EMAIL_TOKEN_EXPIRE_MINUTES") or 30)
ALGORITHM = os.getenv("ALGORITHM") or "HS256"

# Warn when running with default credentials; safe for local dev but insecure in production
if SECRET_KEY == "dev-secret-change-me":
    import warnings
    warnings.warn("Using default SECRET_KEY — set SECRET_KEY via environment in production", RuntimeWarning)
if ADMIN_PASSWORD == "AdminPass123!":
    import warnings
    warnings.warn("Using default ADMIN_PASSWORD — change ADMIN_PASSWORD via environment in production", RuntimeWarning)
LOGIN_TOKEN_EXPIRE_MINUTES = int(os.getenv("LOGIN_TOKEN_EXPIRE_MINUTES") or 60)
# Get the base project directory path
BASE_DIR = Path(__file__).parent

