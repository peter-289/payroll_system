"""Service package exports (compatibility-friendly).

Exports a flat set of commonly-used service names to simplify imports for
existing code while allowing gradual refactor.
"""

from .auth_service import *
from .department_service import *
from .attendance_service import *
from .allowance_service import *
from .deduction_service import *
from .loan_service import *
from .payroll_service import *
from .payroll_engine import *
from .payroll_resolution_service import *
from .pension_service import *
from .salary_service import *
from .tax_service import *
from .user_service import *
from .employee_service import *  # preferred name
from .insuarance_service import *
from .insurance_service import *  # preferred spelling

__all__ = [name for name in globals() if not name.startswith("_")]
