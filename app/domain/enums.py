"""Enumerations for payroll system domain concepts."""
from enum import Enum

class PayFrequency(Enum):
    """Frequency of salary payment."""
    HOURLY = "hourly"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class AttendanceStatus(str, Enum):
    """Status of an attendance record."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class SalaryTypeEnum(str, Enum):
    """Type of salary structure."""
    MONTHLY = "monthly"
    HOURLY = "hourly"
    CONTRACT = "contract"

class GenderEnum(str, Enum):
    """Employee gender options."""
    MALE = "male"
    FEMALE = "female"
    NON_BINARY = "non-binary"


class AllowanceStatus(str, Enum):
    """Status of an allowance record."""
    ACTIVE = "active"
    COMPLETED = "completed"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"

class AllowanceCalculationType(str, Enum):
    """Method for calculating allowance amounts."""
    FIXED = "fixed"
    PERCENTAGE = "percentage"

class AllowancePercentageBasis(str, Enum):
    """Basis for percentage-based allowance calculations."""
    BASIC_SALARY = "basic salary"
    GROSS_SALARY = "gross salary"

class DeductionStatus(str, Enum):
    """Status of a deduction record."""
    ACTIVE = "active"
    COMPLETED = "completed"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"