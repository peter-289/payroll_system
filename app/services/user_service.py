from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
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
from sqlalchemy.exc import SQLAlchemyError
from datetime import date

# import exceptions from centralized exceptions module
from app.domain.exceptions import (
    EmployeeServiceError,
    UserAlreadyExistsError,
    RoleNotFoundError,
    DepartmentNotFoundError,
    PositionNotFoundError,
    ContactAlreadyExistsError,
    BankAccountAlreadyExistsError,
    EmployeeNotFoundError,
    ValidationError,
    AgeValidationError
)
from app.repositories.employee_repo import EmployeeRepository
from app.repositories.role_repo import RoleRepository
from app.repositories.user_repo import UserRepository
from app.repositories.department_repo import DepartmentRepository
from app.repositories.position_repo import PositionRepository
from app.repositories.bank_details_repo import BankRepository
from app.repositories.contacts_repo import ContactRepository
from app.domain.rules.employee_rules import validate_hire_date_not_future,validate_phone_number, validate_salary_type, validate_age


class EmployeeService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.employee_repo = EmployeeRepository(db)
        self.role_repo = RoleRepository(db)
        self.user_repo = UserRepository(db)
        self.department_repo = DepartmentRepository(db)
        self.position_repo = PositionRepository(db)
        self.bank_repo = BankRepository(db)
        self.contact_repo = ContactRepository(db)

    def _check_existing_user(self, username: str) -> None:
        existing_user = self.user_repo.get_user(username)
        if existing_user:
            raise UserAlreadyExistsError(f"Username '{username}' already exists")
        return None
    
    def _check_role(self, rolename: str) -> Role:
        role = self.role_repo.get_role_by_name(rolename)
        if not role:
            raise RoleNotFoundError(f"Role '{rolename}' does not exist")
        return role

    def _check_department(self, department_name: str) -> Department:
        department = self.department_repo.get_department_by_name(department_name)
        if not department:
            raise DepartmentNotFoundError(f"Department '{department_name}' does not exist")
        return department

    def _check_position(self, department_name: str, position_title: str) -> Position:

        department = self.department_repo.get_department_by_name(department_name)
        if not department:
            raise DepartmentNotFoundError(f"Department {department_name} does not exist")
        
        position = self.position_repo.positions_department(department.id)
        if not position:
            raise PositionNotFoundError(f"Position '{position_title}' does not exist in the {department_name} department")
        return position


    def _check_existing_contact(self, email: str) -> None:
        email_contact = self.contact_repo.get_contact(email)
        if email_contact:
            raise ContactAlreadyExistsError(f"Email '{email}' already exists")
        return None

    def _check_bank_details(self, account_number: str) -> None:
        account = self.bank_repo.get_account(account_number)
        if account:
            raise BankAccountAlreadyExistsError(f"Account number '{account_number}' already exists")
        return None
    
    def _create_user(self, employee_data: EmployeeCreate, role_id:int) -> tuple[User, str]:
        if role_id <= 0:
            raise EmployeeServiceError("Invalid ID")
        """Create and return a new User instance"""
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
            
        user = self.user_repo.save(new_user)
        return user, temp_pass
        

    def _create_employee_record(self, user_id:int, department_id:int, position_id:int, data: EmployeeCreate) -> Employee:
        """Create and return a new Employee instance"""
        if user_id <= 0:
            raise EmployeeServiceError("Invalid ID")
        if department_id <= 0:
            raise EmployeeServiceError("Invalid ID")
        if position_id <= 0:
            raise EmployeeServiceError("Invalid ID")
        validate_hire_date_not_future(data.date_hired)
        new_employee = Employee(
            user_id=user_id,
            department_id=department_id,
            position_id=position_id,
            hire_date=data.date_hired or date.today(),
            salary_type=data.salary_type,
        )
        employee = self.employee_repo.temp_save(new_employee)
        return employee

    def _create_employee_contact(self, employee_id:int, data: EmployeeCreate) -> EmployeeContact:
        if employee_id <= 0:
            raise EmployeeServiceError("Invalid ID")
        """Create and return a new EmployeeContact instance"""
        validate_phone_number(data.phone)
        new_contact = EmployeeContact(
            employee_id=employee_id,
            email=data.email,
            phone=data.phone,
            address=data.address,
            city=data.city,
            country=data.country
        )
        self.db.add(new_contact)
        return new_contact

    def _create_employee_bank_account(self, employee_id:int, data: EmployeeCreate) -> EmployeeBankAccount:
        if employee_id <= 0:
            raise EmployeeServiceError("Invalid ID")
        """Create and return a new EmployeeBankAccount instance"""
        bank_account = EmployeeBankAccount(
            employee_id=employee_id,
            bank_name=data.bank_name,
            account_number=data.account_number,
            account_type=data.account_type
        )
        self.db.add(bank_account)
        return bank_account

    def create_employee(self, employee: EmployeeCreate) -> EmployeeCreateResponse:
        """Create a new employee with all associated data"""
        try:
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

            self.db.commit()
            self.db.refresh(new_employee)
      
            return EmployeeCreateResponse(
                employee=new_employee,
                temporary_password=temp_pass
            )

        except (ValidationError, AgeValidationError) as e:
            self.db.rollback()
            print(f"VALIDATION ERROR: {e}")
            raise EmployeeServiceError(f"Employee creation error:{e} ") 
        except SQLAlchemyError as e:
            self.db.rollback()
            raise EmployeeServiceError(f"Unexpected error: {str(e)}")
      
    def get_employee_by_id(self, employee_id: int) -> Employee:
        if employee_id <= 0:
            raise EmployeeServiceError("Invalid ID")
        """Retrieve an employee by ID with related data"""
        employee = self.repo.get_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundError(f"Employee with ID {employee_id} not found")
        return employee
    
    
    def get_employee_position(self, employee_id:int)->Position:
        if employee_id <= 0:
            raise EmployeeServiceError("Invalid ID")
        employee = self.repo.get_by_id(employee_id)
        
        if not employee:
            raise EmployeeNotFoundError(f"Employee with id: {employee_id} not found")
       
        if not employee.position:
            raise EmployeeServiceError(f"No position for employee: {employee_id} was found.")
        return employee.position
    
    def get_employee_department(self, employee_id:int)->Department:
        if employee_id <= 0:
            raise (" Invalid ID")
        employee = self.repo.get_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundError(f"Employee with id: {employee_id} not found.")
        if not employee.department:
            raise EmployeeServiceError(f"No departments associated with employee Id: {employee_id}")
        return employee.department
    
    

    def get_all_employees(self, skip: int = 0, limit: Optional[int] = None) -> List[Employee]:
        """Retrieve all employees with optional pagination"""
        return self.repo.get_all(skip=skip, limit=limit)

    def update_employee(self, employee_id: int, update_data: dict) -> Employee:
        if employee_id <= 0:
            raise EmployeeServiceError("Invalid ID")
        """Update employee information"""
        employee = self.get_employee_by_id(employee_id)
        
        #  Whitelist of updateable fields
        employee_fields = {'salary_type'}
        user_fields = {'first_name', 'last_name', 'gender', 'date_of_birth'}
        
        try:
            for key, value in update_data.items():
                if key in employee_fields and hasattr(employee, key):
                    setattr(employee, key, value)
                elif key in user_fields and hasattr(employee.user, key):
                    setattr(employee.user, key, value)
                # Silently ignore fields not in whitelist
            
            return self.repo.update(employee)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise EmployeeServiceError(f"Failed to update employee: {str(e)}")


    def delete_employee(self, employee_id: int) -> None:
        if employee_id <= 0:
            raise EmployeeServiceError("Invalid ID")
        """Delete an employee and associated user"""
        employee = self.get_employee_by_id(employee_id)
        try:
            self.repo.delete(employee)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise EmployeeServiceError(f"Failed to delete employee: {str(e)}")
        return None
