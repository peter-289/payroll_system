from datetime import date
from app.domain.exceptions.base import DomainError, ValidationError
from app.models.employee_model import SalaryTypeEnum
from datetime import date
from dateutil.relativedelta import relativedelta
import re
from app.domain.exceptions.base import  PhoneValidationError, AgeValidationError, AccountValidationError 



def validate_hire_date_not_future(hire_date: date) -> None:
    """Ensure hire date is not in the future."""
    if hire_date and hire_date > date.today():
        raise DomainError("Hire date cannot be in the future")


def validate_salary_type(salary_type) -> None:
    """Ensure provided salary_type is a valid SalaryTypeEnum value."""
    if salary_type is None:
        return None
    try:
        if isinstance(salary_type, SalaryTypeEnum):
            return None
        # attempt to match by value
        SalaryTypeEnum(salary_type)
    except Exception:
        raise DomainError("Invalid salary type provided")
    

MIN_EMPLOYEE_AGE = 18
MAX_EMPLOYEE_AGE = 65  # retirement age

# Kenyan phone: 07xx xxx xxx or +2547xx xxx xxx
PHONE_REGEX = re.compile(r"^(?:0|254|\+254)7\d{8}$")


ACCOUNT_NUMBER_REGEX = re.compile(r"^[A-Z0-9-]{8,20}$")

def validate_age(date_of_birth: date) -> None:
    """Ensure employee is within working age range (Kenya Labour Laws)"""
    today = date.today()
    age = relativedelta(today, date_of_birth).years
    
    if age < MIN_EMPLOYEE_AGE:
        raise AgeValidationError(f"Employee must be at least {MIN_EMPLOYEE_AGE} years old (born {date_of_birth} → age {age})")
    if age > MAX_EMPLOYEE_AGE:
        raise AgeValidationError(f"Employee age {age} exceeds typical retirement age of {MAX_EMPLOYEE_AGE}")






def validate_phone_number(phone_number: str) -> None:
    """Validate Kenyan mobile number format"""
    phone = phone_number.replace(" ", "").replace("-", "")
    if not PHONE_REGEX.match(phone):
        raise PhoneValidationError(
            f"Invalid Kenyan phone number: {phone_number}. "
            "Must be 07xxxxxxxx, 2547xxxxxxxx, or +2547xxxxxxxx"
        )

def validate_account_number(account_number: str) -> None:
    """Basic validation — can be enhanced per bank"""
    account = account_number.strip().upper()
    if not ACCOUNT_NUMBER_REGEX.match(account):
        raise AccountValidationError(
            f"Invalid account number format: {account_number}. "
            "Must be 8–20 alphanumeric characters or hyphens"
        )

"""

def validate_email(email: str) -> None:
    Validate email format and deliverability
    try:
        validate_email_lib(email.strip(), check_deliverability=False)
    except EmailNotValidError as e:
        raise EmailValidationError(f"Invalid email address: {str(e)}")

"""

def validate_password_strength(new_password: str) -> None:
    """Validate password strength according to defined criteria.""" 
 # Validate password strength
    if len(new_password) < 8:
            raise DomainError("Password must be at least 8 characters long")
    if not any(char.isdigit() for char in new_password):
            raise DomainError("Password must contain at least one digit")
    if not any(char.isupper() for char in new_password):
            raise DomainError("Password must contain at least one uppercase letter")
    if not any(char.islower() for char in new_password):
            raise DomainError("Password must contain at least one lowercase letter")
