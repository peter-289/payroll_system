"""Service for managing user and employee operations."""
from typing import List, Optional
from app.models.user_model import User
from app.models.employee_model import Employee
from app.models.roles_model import Role
from app.models.Position_model import Position
from app.models.department_model import Department
from app.schemas.employee_schema import EmployeeCreate, EmployeeCreateResponse
from app.models.employee_bank_account import EmployeeBankAccount
from app.models.employee_contacts_details import EmployeeContact
from app.core.security import create_temporary_password, parse_date
from app.core.hashing import hash_password
from datetime import date

# import exceptions from centralized exceptions module
from app.domain.exceptions import (
    UserAlreadyExistsError,
    RoleNotFoundError,
    DepartmentNotFoundError,
    PositionNotFoundError,
    ContactAlreadyExistsError,
    BankAccountAlreadyExistsError,
    EmployeeNotFoundError,
    ValidationError
)
from app.core.unit_of_work import UnitOfWork
from app.domain.rules.employee_rules import validate_hire_date_not_future,validate_phone_number, validate_age


class EmployeeService:
    """Service for managing employee-related operations.
    
    Handles employee creation, updates, validation, and bank account/contact management.
    Uses Unit of Work pattern for transaction management.
    """
    def __init__(self, uow: UnitOfWork) -> None:
        """Initialize the employee service.
        
        Args:
            uow: Unit of Work instance for database operations.
        """
        self.uow = uow

    def check_id(self, id_value: int | List[int] | tuple[int, ...]) -> None:
        """Validate that ID or list of IDs are all positive integers.
        
        Args:
            id_value: Single ID, list of IDs, or tuple of IDs to validate.
            
        Raises:
            ValidationError: If any ID is not greater than 0.
        """
        ids = [id_value] if isinstance(id_value, int) else list(id_value) 
        for id_ in ids:
            if id_ <= 0:
                raise ValidationError("Invalid ID")
        return None

    def _check_existing_user(self, username: str) -> None:
        """Check if a username already exists.
        
        Args:
            username: Username to check.
            
        Raises:
            UserAlreadyExistsError: If username is already taken.
        """
        existing_user = self.uow.user_repo.get_user(username)
        if existing_user:
            raise UserAlreadyExistsError(f"Username '{username}' already exists")
        return None
    
    def _check_role(self, rolename: str) -> Role:
        """Verify that a role exists.
        
        Args:
            rolename: The role name to verify.
            
        Returns:
            The Role instance if found.
            
        Raises:
            RoleNotFoundError: If role does not exist.
        """
        role = self.uow.role_repo.get_role_by_name(rolename)
        if not role:
            raise RoleNotFoundError(f"Role '{rolename}' does not exist")
        return role

    def _check_department(self, department_name: str) -> Department:
        """Verify that a department exists.
        
        Args:
            department_name: The department name to verify.
            
        Returns:
            The Department instance if found.
            
        Raises:
            DepartmentNotFoundError: If department does not exist.
        """
        department = self.uow.department_repo.get_department_by_name(department_name)
        if not department:
            raise DepartmentNotFoundError(f"Department '{department_name}' does not exist")
        return department

    def _check_position(self, department_name: str, position_title: str) -> Position:
        """Verify that a position exists in a department.
        
        Args:
            department_name: The department name.
            position_title: The position title to verify.
            
        Returns:
            The Position instance if found.
            
        Raises:
            DepartmentNotFoundError: If department does not exist.
            PositionNotFoundError: If position does not exist in the department.
        """
        department = self._check_department(department_name)
        
        position = self.uow.position_repo.positions_department(department.id)
        if not position:
            raise PositionNotFoundError(f"Position '{position_title}' does not exist in the {department_name} department")
        return position

    def _check_existing_contact(self, email: str) -> None:
        """Check if an email contact already exists.
        
        Args:
            email: Email address to check.
            
        Raises:
            ContactAlreadyExistsError: If email is already registered.
        """
        email_contact = self.uow.contacts_repo.get_contact(email)
        if email_contact:
            raise ContactAlreadyExistsError(f"Email '{email}' already exists")
        return None


    def _check_bank_details(self, account_number: str) -> None:
        """Check if a bank account number exists"""
        account = self.uow.bank_details_repo.get_account(account_number)
        if account:
            raise BankAccountAlreadyExistsError(f"Account number '{account_number}' already exists")
        return None

    
    def _create_user(self, employee_data: EmployeeCreate, role_id:int) -> tuple[User, str]:
        """Create and return a new User instance"""
        self.check_id(role_id)
        temp_pass = create_temporary_password()
        hashed_password = hash_password(temp_pass)
        date_of_birth = parse_date(employee_data.date_of_birth)
        
        validate_age(date_of_birth)

        new_user = User(
               first_name=employee_data.first_name,
               last_name=employee_data.last_name,
               username=employee_data.username,
               gender=employee_data.gender,
               date_of_birth=date_of_birth,
               password_hash=hashed_password,
               role_id=role_id
               )
            
        user = self.uow.user_repo.save(new_user)
        return user, temp_pass
        

    def _create_employee_record(self, user_id:int, department_id:int, position_id:int, data: EmployeeCreate) -> Employee:
        """Create and return a new Employee instance"""
        self.check_id((user_id, department_id, position_id))
        validate_hire_date_not_future(data.date_hired)

        new_employee = Employee(
            user_id=user_id,
            department_id=department_id,
            position_id=position_id,
            hire_date=data.date_hired or date.today(),
            salary_type=data.salary_type,
        )
        employee = self.uow.employee_repo.add_and_flush(new_employee)
        return employee


    def _create_employee_contact(self, employee_id:int, data: EmployeeCreate) -> EmployeeContact:
        """Create and return a new EmployeeContact instance"""
        self.check_id(employee_id)
        validate_phone_number(data.phone)
        new_contact = EmployeeContact(
            employee_id=employee_id,
            email=data.email,
            phone=data.phone,
            address=data.address,
            city=data.city,
            country=data.country
        )
        self.uow.contacts_repo.save(new_contact)
        return new_contact


    def _create_employee_bank_account(self, employee_id:int, data: EmployeeCreate) -> EmployeeBankAccount:
        """Create and return a new EmployeeBankAccount instance"""
        self.check_id(employee_id)
        bank_account = EmployeeBankAccount(
            employee_id=employee_id,
            bank_name=data.bank_name,
            account_number=data.account_number,
            account_type=data.account_type
        )
        self.uow.bank_details_repo.save(bank_account)
        return bank_account


    def create_employee(self, employee: EmployeeCreate) -> EmployeeCreateResponse:
        """Create a new employee with all associated data"""
        with self.uow:      
            # Data validation before db operations
            self._check_existing_user(employee.username)
            role = self._check_role(employee.role_name)
            department = self._check_department(employee.department_name)
            position = self._check_position(employee.department_name, employee.position_title)
            self._check_existing_contact(employee.email)
            self._check_bank_details(employee.account_number)

            # Create user
            new_user, temp_pass = self._create_user(employee, role.id)

            # Create employee record
            new_employee = self._create_employee_record(new_user.id, department.id, position.id, employee)

            # Create contact information
            self._create_employee_contact(new_employee.id, employee)

            # Create bank account
            self._create_employee_bank_account(new_employee.id, employee)
            # Audit log
            self.uow.audit_repo.log_action(
                user_id=new_user.id,
                action=f"Created employee {new_employee.id} with user {new_user.username}",
                metadata={"employee_id": new_employee.id, "username": new_user.username}
            )
            return EmployeeCreateResponse(
                employee=new_employee,
                temporary_password=temp_pass
                )
            
            
    
    def get_employee_by_id(self, employee_id: int) -> Employee:
        """Retrieve an employee by ID with related data"""
        self.check_id(employee_id)
        employee = self.uow.employee_repo.get_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundError(f"Employee with ID {employee_id} not found")
        self.uow.audit_repo.log_action(
            user_id=employee.user_id,
            action=f"Retrieved employee {employee_id}",
            metadata={"employee_id": employee_id}
        )
        return employee
    
    
    def get_employee_position(self, employee_id:int)->Position:
        """Get an employee's position by ID"""
        self.check_id(employee_id)
        employee = self.uow.employee_repo.get_by_id(employee_id)
        
        if not employee:
            raise EmployeeNotFoundError(f"Employee with id: {employee_id} not found")
        if not employee.position:
            raise PositionNotFoundError(f"No position for employee: {employee_id} was found.")
        self.uow.audit_repo.log_action(
            user_id=employee.user_id,
            action=f"Retrieved position for employee {employee_id}",
            metadata={"employee_id": employee_id}
        )
        return employee.position
    

    def get_employee_department(self, employee_id:int)->Department:
        """Retrieve an employee's department by ID"""
        self.check_id(employee_id)
        employee = self.uow.employee_repo.get_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundError(f"Employee with id: {employee_id} not found.")
        if not employee.department:
            raise DepartmentNotFoundError(f"No departments associated with employee Id: {employee_id}")
        self.uow.audit_repo.log_action(
            user_id=employee.user_id,
            action=f"Retrieved department for employee {employee_id}",
            metadata={"employee_id": employee_id}
        )
        return employee.department
    
    

    def get_all_employees(self, skip: int = 0, limit: Optional[int] = None) -> List[Employee]:
        """Retrieve all employees with optional pagination"""
        return self.uow.employee_repo.get_all_employees(skip=skip, limit=limit)


    def update_employee(self, employee_id: int, update_data: dict) -> Employee:
        """Update employee information"""
        self.check_id(employee_id)
        employee = self.get_employee_by_id(employee_id)
        
        #  Whitelist of updateable fields
        employee_fields = {'salary_type'}
        user_fields = {'first_name', 'last_name', 'gender', 'date_of_birth'}
        
        with self.uow:
             for key, value in update_data.items():
                if key in employee_fields and hasattr(employee, key):
                    setattr(employee, key, value)
                elif key in user_fields and hasattr(employee.user, key):
                    setattr(employee.user, key, value)

                # Silently ignore fields not in whitelist
                self.uow.employee_repo.update(employee)
                self.uow.audit_repo.log_action(
                    user_id=employee.user_id,
                    action=f"Updated employee {employee_id}",
                    metadata={"employee_id": employee_id, "updated_fields": list(update_data.keys())}
                )
                return employee


    def delete_employee(self, employee_id: int) -> None:
        """Delete an employee and associated user"""
        self.check_id(employee_id)
        employee = self.get_employee_by_id(employee_id)
        with self.uow:
            self.uow.employee_repo.delete(employee)
            self.uow.audit_repo.log_action(
                user_id=employee.user_id,
                action=f"Deleted employee {employee_id}",
                metadata={"employee_id": employee_id}
        )
        return None
