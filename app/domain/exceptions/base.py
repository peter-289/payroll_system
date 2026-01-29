"""Domain layer exceptions for the payroll system.

All domain exceptions inherit from DomainError and represent business logic violations.
These exceptions should be caught by the service layer and converted to API responses.
"""
from typing import Any
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


# =======================================================================================================
#-------------------- DOMAIN BASE EXCEPTIONS -----------------------------------------------------
class DomainError(Exception):
    """Base exception for all domain errors.
    
    This is the root exception for all domain layer errors. Services should catch
    this exception and convert it to appropriate HTTP responses.
    """
    def __init__(self, message: str | None = None):
        """Initialize domain error with message.
        
        Args:
            message: Error message describing what went wrong.
        """
        super().__init__(message or "Domain error")

class NotFoundError(DomainError):
    """Exception raised when a requested resource is not found in the domain."""
    pass

class ConflictError(DomainError):
    """Exception raised when a domain operation conflicts with existing state."""
    pass

class ValidationError(DomainError):
    """Exception raised when domain data fails validation rules."""
    pass

class PermissionError(DomainError):
    """Exception raised when a user lacks required permissions for an operation."""
    pass

class ComputationError(DomainError):
    """Exception raised when domain computation/calculation fails."""
    pass

#===============================================================================================
#---------------- VALIDATION EXCEPTIONS -------------------------------------------------------
class EmailValidationError(ValidationError):
    """Exception raised when email validation fails."""
    pass

class PhoneValidationError(ValidationError):
    """Exception raised when phone number validation fails."""
    pass

class AgeValidationError(ValidationError):
    """Exception raised when age validation fails."""
    pass

class AccountValidationError(ValidationError):
    """Exception raised when account-related validation fails."""
    pass




#=============================================================================================
#-------------------- EMPLOYEE SERVICE EXCEPTIONS --------------------------------------------
class UserAlreadyExistsError(ConflictError):
    pass

class RoleNotFoundError(NotFoundError):
    pass

class DepartmentNotFoundError(NotFoundError):
    pass

class PositionNotFoundError(NotFoundError):
    pass

class ContactAlreadyExistsError(ConflictError):
    pass

class BankAccountAlreadyExistsError(ConflictError):
    pass

class EmployeeNotFoundError(NotFoundError):
    pass


#==============================================================================================
#------------------ PAYROLL ENGINE EXCEPTIONS -------------------------------------------------
class PayrollEngineError(Exception):
    """Base exception for payroll engine"""
    def __init__(self, message: str | None = None, payload: Any | None = None):
        super().__init__(message or "Payroll engine error")
        self.payload = payload


class InvalidPayrollInputError(PayrollEngineError):
    pass

class TaxCalculationError(PayrollEngineError):
    pass


# =============================================================================================
#-------------------- DEPARTMENT SERVICE EXCEPTIONS ------------------------------------------
class DepartmentAlreadyExistsError(ConflictError):
    """Raised when department with same name already exists"""
    pass


# =============================================================================================
#-------------------- TAX SERVICE EXCEPTIONS ---------------------------------------------------
class TaxRuleNotFoundError(NotFoundError):
    pass

class InvalidTaxBracketsError(ValidationError):
    pass




# ========================================================================================
# -------------- ALLOWANCE SERVICE EXCEPTIONS --------------------------------------------
class AllowanceTypeNotFoundError(NotFoundError):
    pass

class AllowanceRecordNotFoundError(NotFoundError):
      pass


#=============================================================================================
#-------------------- ATTENDANCE SERVICE EXCEPTIONS ------------------------------------------
class AttendanceRecordNotFoundError(NotFoundError):
    pass

class FutureCheckInError(ValidationError):
    pass

class InvalidTimeRangeError(ValidationError):
    pass

class OverlappingAttendanceError(ValidationError):
    pass

class OpenAttendanceExistsError(ValidationError):
    pass

class AttendanceNotApprovedError(ValidationError):
    pass

class AttendanceAlreadyApprovedError(ValidationError):
    pass

class AttendanceAlreadyExistsError(ValidationError):
    pass

class CanNotCheckoutError(ValidationError):
    pass


# =============================================================================================
#-------------------- INSURANCE SERVICE EXCEPTIONS -----------------------------------------
class InsuranceRecordNotFoundError(NotFoundError):
    pass


# =============================================================================================
#-------------------- AUTHENTICATION & USER SERVICE EXCEPTIONS --------------------------------
class InvalidCredentialsError(ValidationError):
    pass

class TokenExpiredError(ValidationError):
    pass

class InvalidTokenError(ValidationError):
    pass

class UserNotFoundError(NotFoundError):
    pass


#=============================================================================================
#-------------------- SALARY SERVICE EXCEPTIONS ------------------------------------------------
class SalaryNotFoundError(NotFoundError):
    pass


class InvalidPayFrequencyError(ValidationError):
    """Raised when an unsupported pay frequency is supplied to payroll engines"""
    pass


# =============================================================================================
#-------------------- DEDUCTION SERVICE EXCEPTIONS ---------------------------------------------
class DeductionNotFoundError(NotFoundError):
    pass


# =============================================================================================
#-------------------- PENSION SERVICE EXCEPTIONS ------------------------------------------------
class PensionNotFoundError(NotFoundError):
    pass


# =============================================================================================
#-------------------- LOAN SERVICE EXCEPTIONS ---------------------------------------------------
class LoanNotFoundError(NotFoundError):
    pass


#=============================================================================================
#-------------------- PAYROLL EXCEPTIONS -----------------------------------------------------
class PayrollComputeError(Exception):
    """Exception for payroll computation errors"""
    def __init__(self, message: str | None = None):
        super().__init__(message or "Payroll computation error")

# =============================================================================================
#-------------------- PAYROLL RUN EXCEPTIONS -------------------------------------------------
class PayrollRunError(Exception):
    """Raised when a payroll run cannot be completed (business/domain level)."""
    pass



# =============================================================================================
#-------------------- DOMAIN ERROR TRANSLATION ------------------------------------------------
class DomainErrorTranslator:
    """Translates domain exceptions to HTTP exceptions."""

    @staticmethod
    def translate(exception: DomainError) -> HTTPException:
        """Translate a DomainError into an appropriate HTTPException."""
        if isinstance(exception, NotFoundError):
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exception)})
        elif isinstance(exception, ConflictError):
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exception)})
        elif isinstance(exception, ValidationError):
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exception)})
        elif isinstance(exception, PermissionError):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": str(exception)})
        else:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": str(exception)})
            