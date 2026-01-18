from enum import Enum

class PayFrequency(Enum):
    HOURLY = "hourly"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class AttendanceStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class SalaryTypeEnum(str, Enum):
    MONTHLY = "monthly"
    HOURLY = "hourly"
    CONTRACT = "contract"

class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    NONB_INARY = "non-binary"


class AllowanceStatus(str, Enum):
    """Status of allowance."""
    ACTIVE = "active"
    COMPLETED = "completed"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"

class AllowanceCalculationType(str, Enum):
    """ Calculation basis """
    FIXED = "fixed"
    PERCENTAGE = "percentage"

class AllowancePercentageBasis(str, Enum):
    """If an allowance is a percentage."""
    BASIC_SALARY = "basic salary"
    GROSS_SALARY = "gross salary"

class DeductionStatus(str, Enum):
    """Status of deduction."""
    ACTIVE = "active"
    COMPLETED = "completed"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"