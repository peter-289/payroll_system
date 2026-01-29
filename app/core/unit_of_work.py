from sqlalchemy.orm import Session
from app.repositories.attendance_repo import AttendanceRepository
from app.repositories.employee_repo import EmployeeRepository
from app.repositories.user_repo import UserRepository
from app.repositories.department_repo import DepartmentRepository
from app.repositories.position_repo import PositionRepository
from app.repositories.salary_repo import SalaryRepository
from app.repositories.allowance_repo import AllowanceRepository
from app.repositories.deduction_repo import DeductionRepository
from app.repositories.payroll_repo import PayrollRepository
from app.repositories.role_repo import RoleRepository
from app.repositories.contacts_repo import ContactsRepository
from app.repositories.bank_details_repo import BankDetailsRepository
from app.repositories.insurance_repo import InsuranceRepository
from app.repositories.audit_repo import AuditRepository
from app.repositories.loan_repository import LoanRepository


class UnitOfWork:
    """Unit of Work pattern implementation for managing database transactions.
    
    Provides centralized access to all repositories and manages transaction boundaries
    (commit/rollback). Uses lazy-loading to instantiate repositories only when needed.
    Supports context manager protocol for automatic transaction handling.
    """
    def __init__(self, session: Session):
        """Initialize the UnitOfWork with a database session.
        
        Args:
            session: SQLAlchemy session object for database operations.
        """
        self.session = session
        self._attendance_repo = None
        self._employee_repo = None
        self._user_repo = None
        self._department_repo = None
        self._position_repo = None
        self._salary_repo = None
        self._allowance_repo = None
        self._deduction_repo = None
        self._payroll_repo = None
        self._role_repo = None
        self._contacts_repo = None
        self._bank_details_repo = None
        self._insurance_repo = None
        self._audit_repo = None
        self._loan_repo = None

    @property
    def attendance_repo(self) -> AttendanceRepository:
        if self._attendance_repo is None:
            self._attendance_repo = AttendanceRepository(self.session)
        return self._attendance_repo

    @property
    def employee_repo(self) -> EmployeeRepository:
        if self._employee_repo is None:
            self._employee_repo = EmployeeRepository(self.session)
        return self._employee_repo

    @property
    def user_repo(self) -> UserRepository:
        if self._user_repo is None:
            self._user_repo = UserRepository(self.session)
        return self._user_repo

    @property
    def department_repo(self) -> DepartmentRepository:
        if self._department_repo is None:
            self._department_repo = DepartmentRepository(self.session)
        return self._department_repo

    @property
    def position_repo(self) -> PositionRepository:
        if self._position_repo is None:
            self._position_repo = PositionRepository(self.session)
        return self._position_repo

    @property
    def salary_repo(self) -> SalaryRepository:
        if self._salary_repo is None:
            self._salary_repo = SalaryRepository(self.session)
        return self._salary_repo

    @property
    def allowance_repo(self) -> AllowanceRepository:
        if self._allowance_repo is None:
            self._allowance_repo = AllowanceRepository(self.session)
        return self._allowance_repo

    @property
    def deduction_repo(self) -> DeductionRepository:
        if self._deduction_repo is None:
            self._deduction_repo = DeductionRepository(self.session)
        return self._deduction_repo

    @property
    def payroll_repo(self) -> PayrollRepository:
        if self._payroll_repo is None:
            self._payroll_repo = PayrollRepository(self.session)
        return self._payroll_repo

    @property
    def role_repo(self) -> RoleRepository:
        if self._role_repo is None:
            self._role_repo = RoleRepository(self.session)
        return self._role_repo

    @property
    def contacts_repo(self) -> ContactsRepository:
        if self._contacts_repo is None:
            self._contacts_repo = ContactsRepository(self.session)
        return self._contacts_repo

    @property
    def bank_details_repo(self) -> BankDetailsRepository:
        if self._bank_details_repo is None:
            self._bank_details_repo = BankDetailsRepository(self.session)
        return self._bank_details_repo

    @property
    def insurance_repo(self) -> InsuranceRepository:
        if self._insurance_repo is None:
            self._insurance_repo = InsuranceRepository(self.session)
        return self._insurance_repo

    @property
    def audit_repo(self) -> AuditRepository:
        if self._audit_repo is None:
            self._audit_repo = AuditRepository(self.session)
        return self._audit_repo
    
    @property
    def loan_repo(self) -> LoanRepository:
        if self._loan_repo is None:
            self._loan_repo = LoanRepository(self.session)
        return self._loan_repo
    
    def commit(self) -> None:
        """Commit the current transaction to the database."""
        self.session.commit()

    def rollback(self) -> None:
        """Rollback the current transaction, undoing all pending changes."""
        self.session.rollback()

    def __enter__(self):
        """Enter context manager - returns self for use in with statement."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager - automatically commits or rollbacks transaction.
        
        Args:
            exc_type: Exception type if an exception occurred.
            exc_val: Exception value if an exception occurred.
            exc_tb: Exception traceback if an exception occurred.
            
        If an exception occurred, the transaction is rolled back.
        Otherwise, the transaction is committed.
        """
        if exc_type:
            self.rollback()
        else:
            self.commit()
