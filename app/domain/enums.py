from enum import Enum

class PayFrequency(Enum):
    HOURLY = "hourly"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class AttendanceStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


