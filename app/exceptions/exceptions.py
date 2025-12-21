from typing import Any


class EmployeeServiceError(Exception):
    """Base exception for employee service errors"""
    def __init__(self, message: str | None = None):
        super().__init__(message or "Employee service error")


class UserAlreadyExistsError(EmployeeServiceError):
    pass


class RoleNotFoundError(EmployeeServiceError):
    pass


class DepartmentNotFoundError(EmployeeServiceError):
    pass


class PositionNotFoundError(EmployeeServiceError):
    pass


class ContactAlreadyExistsError(EmployeeServiceError):
    pass


class BankAccountAlreadyExistsError(EmployeeServiceError):
    pass


class EmployeeNotFoundError(EmployeeServiceError):
    pass


# Payroll related exceptions
class PayrollEngineError(Exception):
    """Base exception for payroll engine"""
    def __init__(self, message: str | None = None, payload: Any | None = None):
        super().__init__(message or "Payroll engine error")
        self.payload = payload


class InvalidPayrollInputError(PayrollEngineError):
    pass


class TaxCalculationError(PayrollEngineError):
    pass

# Department related exceptions
class DepartmentServiceError(Exception):
    """Base exception for department service errors"""
    def __init__(self, message: str | None = None):
        super().__init__(message or "Department service error")


class DepartmentAlreadyExistsError(DepartmentServiceError):
    """Raised when department with same name already exists"""
    pass


# Tax related exceptions
class TaxServiceError(Exception):
    """Base exception for tax service errors"""
    def __init__(self, message: str | None = None):
        super().__init__(message or "Tax service error")


class TaxRuleNotFoundError(TaxServiceError):
    pass


class InvalidTaxBracketsError(TaxServiceError):
    pass


# Attendance related exceptions
class AttendanceServiceError(Exception):
    """Base exception for attendance service errors"""
    def __init__(self, message: str | None = None):
        super().__init__(message or "Attendance service error")


class AttendanceRecordNotFoundError(AttendanceServiceError):
    pass


# Allowance related exceptions
class AllowanceServiceError(Exception):
    """Base exception for allowance service errors"""
    def __init__(self, message: str | None = None):
        super().__init__(message or "Allowance service error")


class AllowanceTypeNotFoundError(AllowanceServiceError):
    pass


class AllowanceRecordNotFoundError(AllowanceServiceError):
    pass


# Insurance related exceptions
class InsuranceServiceError(Exception):
    """Base exception for insurance service errors"""
    def __init__(self, message: str | None = None):
        super().__init__(message or "Insurance service error")


class InsuranceRecordNotFoundError(InsuranceServiceError):
    pass


# Auth related exceptions
class AuthServiceError(Exception):
    """Base exception for auth service errors"""
    def __init__(self, message: str | None = None):
        super().__init__(message or "Authentication error")


class InvalidCredentialsError(AuthServiceError):
    pass


class TokenExpiredError(AuthServiceError):
    pass


class UserNotFoundError(AuthServiceError):
    pass


# Salary related exceptions
class SalaryServiceError(Exception):
    """Base exception for salary service errors"""
    def __init__(self, message: str | None = None):
        super().__init__(message or "Salary service error")


class SalaryNotFoundError(SalaryServiceError):
    pass


# Deduction related exceptions
class DeductionServiceError(Exception):
    """Base exception for deduction service errors"""
    def __init__(self, message: str | None = None):
        super().__init__(message or "Deduction service error")


class DeductionNotFoundError(DeductionServiceError):
    pass


# Pension related exceptions
class PensionServiceError(Exception):
    """Base exception for pension service errors"""
    def __init__(self, message: str | None = None):
        super().__init__(message or "Pension service error")


class PensionNotFoundError(PensionServiceError):
    pass


# Loan related exceptions
class LoanServiceError(Exception):
    """Base exception for loan service errors"""
    def __init__(self, message: str | None = None):
        super().__init__(message or "Loan service error")


class LoanNotFoundError(LoanServiceError):
    pass