import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.exceptions.exceptions import (
    UserAlreadyExistsError,
    EmployeeNotFoundError,
    RoleNotFoundError,
    DepartmentNotFoundError,
    PositionNotFoundError,
)


def test_exception_definitions():
    """Test that all exception classes are properly defined."""
    # Test creating exception instances
    exc = UserAlreadyExistsError("Username exists")
    assert str(exc) == "Username exists"
    
    exc2 = EmployeeNotFoundError("Employee not found")
    assert "Employee not found" in str(exc2)
    
    # Test inheritance
    from app.exceptions.exceptions import EmployeeServiceError
    assert issubclass(UserAlreadyExistsError, EmployeeServiceError)
    assert issubclass(RoleNotFoundError, EmployeeServiceError)
    print("✓ All exception classes properly defined")


def test_payroll_exceptions():
    """Test payroll-specific exceptions."""
    from app.exceptions.exceptions import PayrollEngineError, InvalidPayrollInputError
    
    exc = InvalidPayrollInputError("No earnings provided")
    assert "No earnings provided" in str(exc)
    assert issubclass(InvalidPayrollInputError, PayrollEngineError)
    print("✓ Payroll exception classes work correctly")
