from app.domain.exceptions.base import AttendanceServiceError,CanNotCheckoutError,AttendanceAlreadyExistsError, FutureCheckInError,AttendanceAlreadyApprovedError, InvalidTimeRangeError, AttendanceNotApprovedError
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Optional
from app.domain.enums import AttendanceStatus


MAX_REGULAR_WORKING_HOURS = Decimal("8.0")
MAX_OVERTIME_HOURS = Decimal("4.0")
MAX_WORKING_HOURS_PER_DAY = MAX_REGULAR_WORKING_HOURS + MAX_OVERTIME_HOURS
LATE_ARRIVAL_CUTTOFF = datetime.strptime("9:00","%H:%M").time()



def validate_check_in_time(check_in: datetime, today: date)->None:
    if check_in.date() > today:
        raise FutureCheckInError("Can not check in for a future date")
    
def ensure_not_duplicate(existing_attendance)-> None:
    if existing_attendance is not None:
        raise AttendanceAlreadyExistsError("Attendance for this employee exists")

def validate_checkout(check_in: datetime, check_out: datetime)->None:
    if check_out and check_out <= check_in:
        raise InvalidTimeRangeError("Check-out must be after check in")
    


def ensure_can_be_proved(attendance) -> None:
    if attendance is None:
        raise AttendanceServiceError("Attendance record not found for the given date")
    
    if attendance.approved == AttendanceStatus.APPROVED:
        raise AttendanceServiceError("Cannot modify already approved attendance")
    
def ensure_can_checkout(attendance):
    if attendance.check_in is None:
        raise CanNotCheckoutError("No check-in so can not check-out")
    
def validate_overtime_hours(overtime_hours: Optional[Decimal])->None:
    if overtime_hours is None:
        overtime_hours = Decimal("0")
    if overtime_hours < 0:
        raise AttendanceServiceError("Overtime hours can not be 0 or negative")
    if overtime_hours > MAX_OVERTIME_HOURS:
        raise AttendanceServiceError(f"Overtime hours can not exceed {MAX_OVERTIME_HOURS} per day")


def check_late_arrival(check_in:datetime)->None:
    return check_in.time() > LATE_ARRIVAL_CUTTOFF


def validate_total_working_hours(hours_worked:Decimal)->None:
    if hours_worked > MAX_WORKING_HOURS_PER_DAY:
        raise AttendanceServiceError(f"Total working hours can not exceed {MAX_WORKING_HOURS_PER_DAY}")

def deny_recheckout(attendance)->None:
    if attendance.check_out:
        raise AttendanceAlreadyExistsError("Can not re-checkout")

def check_approved(approved:bool | None):
    if approved is not True:
        raise AttendanceNotApprovedError("Attendance not approved")


def calculate_hours(check_in: Optional[datetime], check_out:Optional[datetime])-> Decimal:
    if not check_in or not check_out:
       return Decimal('0')
    if check_out <= check_in:
        return Decimal('0')
    
    delta = check_out - check_in
    total_seconds = Decimal(delta.total_seconds())
    total_hours = total_seconds/Decimal('3600')

    return total_hours.quantize(Decimal('0.01'))


def split_regular_and_overtime(total_hours: Decimal) -> tuple[Decimal, Decimal]:
    regular = min(total_hours, MAX_REGULAR_WORKING_HOURS)
    overtime = max(Decimal('0'), total_hours - MAX_REGULAR_WORKING_HOURS)
    return regular, overtime