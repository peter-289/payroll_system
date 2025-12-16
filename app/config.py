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
LOGIN_TOKEN_EXPIRE_MINUTES = int(os.getenv("LOGIN_TOKEN_EXPIRE_MINUTES") or 60)
# Get the base project directory path
BASE_DIR = Path(__file__).parent


#------------------------------------------------------------------------------------------------------
# ------------------------------ EMAIL CONFIG ---------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
#mail_config = ConnectionConfig(
   # MAIL_USERNAME=os.getenv("EMAIL_USERNAME", ""),
    #