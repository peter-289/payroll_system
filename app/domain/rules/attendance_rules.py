from app.domain.exceptions.base import DomainError,CanNotCheckoutError,AttendanceAlreadyExistsError, FutureCheckInError,AttendanceAlreadyApprovedError, InvalidTimeRangeError, AttendanceNotApprovedError
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Optional
from app.domain.enums import AttendanceStatus


MAX_REGULAR_WORKING_HOURS = Decimal("8.0")
MAX_OVERTIME_HOURS = Decimal("4.0")
MAX_WORKING_HOURS_PER_DAY = MAX_REGULAR_WORKING_HOURS + MAX_OVERTIME_HOURS
LATE_ARRIVAL_CUTTOFF = datetime.strptime("9:00","%H:%M").time()



def validate_check_in_time(check_in: datetime, today: date)->None:
    """Validate check-in time"""
    if check_in.date() > today:
        raise FutureCheckInError("Can not check in for a future date")
    
def ensure_not_duplicate(existing_attendance)-> None:
    """Ensure no duplicate attendance record exists"""
    if existing_attendance is not None:
        raise AttendanceAlreadyExistsError("Attendance for this employee exists")

def validate_checkout(check_in: datetime, check_out: datetime)->None:
    """Validate check-out time"""
    if check_out and check_out <= check_in:
        raise InvalidTimeRangeError("Check-out must be after check in")
    


def ensure_can_be_proved(attendance) -> None:
    """Ensure attendance can be approved"""
    if attendance is None:
        raise DomainError("Attendance record not found for the given date")
    
    if attendance.approved == AttendanceStatus.APPROVED:
        raise DomainError("Cannot modify already approved attendance")
    
def ensure_can_checkout(attendance):
    """Ensure attendance can be checked out"""
    if attendance.check_in is None:
        raise CanNotCheckoutError("No check-in so can not check-out")
    
def validate_overtime_hours(overtime_hours: Optional[Decimal])->None:
    """Validate overtime hours"""
    if overtime_hours is None:
        overtime_hours = Decimal("0")
    if overtime_hours < 0:
        raise DomainError("Overtime hours can not be 0 or negative")
    if overtime_hours > MAX_OVERTIME_HOURS:
        raise DomainError(f"Overtime hours can not exceed {MAX_OVERTIME_HOURS} per day")


def check_late_arrival(check_in:datetime)->None:
    """Check if check-in time is late"""
    return check_in.time() > LATE_ARRIVAL_CUTTOFF


def validate_total_working_hours(hours_worked:Decimal)->None:
    """Validate total working hours"""
    if hours_worked > MAX_WORKING_HOURS_PER_DAY:
        raise DomainError(f"Total working hours can not exceed {MAX_WORKING_HOURS_PER_DAY}")

def deny_recheckout(attendance)->None:
    """Deny re-checkout if already checked out"""
    if attendance.check_out:
        raise AttendanceAlreadyExistsError("Can not re-checkout")

def check_approved(approved:bool | None):
    """Check if attendance is approved"""
    if approved is not True:
        raise AttendanceNotApprovedError("Attendance not approved")


def calculate_hours(check_in: Optional[datetime], check_out:Optional[datetime])-> Decimal:
    """Calculate total hours worked between check-in and check-out"""
    if not check_in or not check_out:
       return Decimal('0')
    if check_out <= check_in:
        return Decimal('0')
    
    delta = check_out - check_in
    total_seconds = Decimal(delta.total_seconds())
    total_hours = total_seconds/Decimal('3600')

    return total_hours.quantize(Decimal('0.01'))


def split_regular_and_overtime(total_hours: Decimal) -> tuple[Decimal, Decimal]:
    """Split total hours into regular and overtime hours"""
    regular = min(total_hours, MAX_REGULAR_WORKING_HOURS)
    overtime = max(Decimal('0'), total_hours - MAX_REGULAR_WORKING_HOURS)
    return regular, overtime