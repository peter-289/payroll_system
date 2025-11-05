import os
from pathlib import Path
from fastapi_mail import ConnectionConfig
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # dotenv not available — rely on environment variables or defaults
    pass

# Default to a local SQLite file if DATABASE_URL not provided
DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///./payroll.db"

# SECRET_KEY should be set in environment for production. Provide a default for local/dev use.
SECRET_KEY = os.getenv("SECRET_KEY") or "dev-secret-change-me"

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME") or "admin"
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL") or "admin@example.com"
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD") or "AdminPass123!"
EMAIL_TOKEN_EXPIRE_MINUTES = int(os.getenv("EMAIL_TOKEN_EXPIRE_MINUTES") or 30)
ALGORITHM = os.getenv("ALGORITHM") or "HS256"

# Get the base project directory path
BASE_DIR = Path(__file__).parent

# Email configuration
mail_config = ConnectionConfig(
    MAIL_USERNAME=os.getenv("EMAIL_USERNAME", ""),
    MAIL_PASSWORD=os.getenv("EMAIL_PASSWORD", ""),
    MAIL_FROM=os.getenv("EMAIL_FROM", "tech_pulse@techpulse.com"),
    MAIL_PORT=int(os.getenv("EMAIL_PORT", "1025")),
    MAIL_SERVER=os.getenv("EMAIL_HOST", "localhost"),
    MAIL_STARTTLS=os.getenv("EMAIL_USE_TLS", "false").lower() == "true",
    MAIL_SSL_TLS=os.getenv("EMAIL_USE_SSL", "false").lower() == "true",
    USE_CREDENTIALS=bool(os.getenv("EMAIL_USERNAME")), # Only use credentials if username is set
    VALIDATE_CERTS=os.getenv("EMAIL_USE_TLS", "false").lower() == "true",
    TEMPLATE_FOLDER=BASE_DIR / "UI" / "email_templates"  # Set absolute path to templates
)