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
from app.dependancies.security import hash_password, create_temporary_password, parse_date
from sqlalchemy.exc import SQLAlchemyError
from datetime import date

# import exceptions from centralized exceptions module
from app.exceptions.exceptions import (
    EmployeeServiceError,
    UserAlreadyExistsError,
    RoleNotFoundError,
    DepartmentNotFoundError,
    PositionNotFoundError,
    ContactAlreadyExistsError,
    BankAccountAlreadyExistsError,
    EmployeeNotFoundError,
)
 




class EmployeeService:
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def _check_existing_user(self, username: str) -> None:
        existing_user = self.db.query(User).filter(User.username == username).first()
        if existing_user:
            raise UserAlreadyExistsError(f"Username '{username}' already exists")
        return None
    
    def _check_role(self, rolename: str) -> Role:
        role = self.db.query(Role).filter(Role.role_name == rolename).first()
        if not role:
            raise RoleNotFoundError(f"Role '{rolename}' does not exist")
        return role

    def _check_department(self, department_name: str) -> Department:
        department = self.db.query(Department).filter(Department.name == department_name).first()
        if not department:
            raise DepartmentNotFoundError(f"Department '{department_name}' does not exist")
        return department

    def _check_position(self, position_name: str, department_name: str) -> Position:
        department = self._check_department(department_name)
        position = self.db.query(Position).filter(
            Position.title == position_name,
            Position.department_id == department.id).first()
        if not position:
            raise PositionNotFoundError(f"Position '{position_name}' does not exist in '{department_name}' department")
        return position

    def _check_existing_contact(self, email: str, phone: str) -> None:
        email_contact = self.db.query(EmployeeContact).filter(EmployeeContact.email == email).first()
        phone_contact = self.db.query(EmployeeContact).filter(EmployeeContact.phone == phone).first()
        if email_contact:
            raise ContactAlreadyExistsError(f"Email '{email}' already exists")
        if phone_contact:
            raise ContactAlreadyExistsError(f"Phone number '{phone}' already exists")
        return None

    def _check_bank_details(self, account_number: str) -> None:
        account = self.db.get(EmployeeBankAccount, account_number)
        if account:
            raise BankAccountAlreadyExistsError(f"Account number '{account_number}' already exists")
        return None
    
    def _create_user(self, employee_data: EmployeeCreate, role: Role) -> tuple[User, str]:
        """Create and return a new User instance"""
        temp_pass = create_temporary_password()
        hashed_password = hash_password(temp_pass)
        date_of_birth = parse_date(employee_data.date_of_birth)

        new_user = User(
            first_name=employee_data.first_name,
            last_name=employee_data.last_name,
            username=employee_data.username,
            gender=employee_data.gender,
            date_of_birth=date_of_birth,
            password_hash=hashed_password,
            role_id=role.id
        )
        self.db.add(new_user)
        self.db.flush()
        return new_user, temp_pass

    def _create_employee_record(self, user: User, department: Department, position: Position, employee_data: EmployeeCreate) -> Employee:
        """Create and return a new Employee instance"""
        new_employee = Employee(
            user_id=user.id,
            department_id=department.id,
            position_id=position.id,
            hire_date=employee_data.date_hired or date.today(),
            salary_type=employee_data.salary_type,
        )
        self.db.add(new_employee)
        self.db.flush()
        return new_employee

    def _create_employee_contact(self, employee: Employee, employee_data: EmployeeCreate) -> EmployeeContact:
        """Create and return a new EmployeeContact instance"""
        new_contact = EmployeeContact(
            employee_id=employee.id,
            email=employee_data.email,
            phone=employee_data.phone,
            address=employee_data.address,
            city=employee_data.city,
            country=employee_data.country
        )
        self.db.add(new_contact)
        return new_contact

    def _create_employee_bank_account(self, employee: Employee, employee_data: EmployeeCreate) -> EmployeeBankAccount:
        """Create and return a new EmployeeBankAccount instance"""
        new_bank_account = EmployeeBankAccount(
            employee_id=employee.id,
            bank_name=employee_data.bank_name,
            account_number=employee_data.account_number,
            account_type=employee_data.account_type
        )
        self.db.add(new_bank_account)
        return new_bank_account

    def create_employee(self, employee: EmployeeCreate) -> EmployeeCreateResponse:
        """Create a new employee with all associated data"""
        # Validate all data before any database operations
        self._check_existing_user(employee.username)
        role = self._check_role(employee.role_name)
        department = self._check_department(employee.department_name)
        position = self._check_position(employee.position_title, employee.department_name)
        self._check_existing_contact(employee.email, employee.phone)
        self._check_bank_details(employee.account_number)

        try:
            # Create user
            new_user, temp_pass = self._create_user(employee, role)

            # Create employee record
            new_employee = self._create_employee_record(new_user, department, position, employee)

            # Create contact information
            self._create_employee_contact(new_employee, employee)

            # Create bank account
            self._create_employee_bank_account(new_employee, employee)

            self.db.commit()
            self.db.refresh(new_employee)

            return EmployeeCreateResponse(
                employee=new_employee,
                temporary_password=temp_pass
            )

        except EmployeeServiceError:
            self.db.rollback()
            raise
        except SQLAlchemyError as e:
            self.db.rollback()
            raise EmployeeServiceError(f"Failed to create employee: {str(e)}")
        except Exception as e:
            self.db.rollback()
            raise EmployeeServiceError(f"Unexpected error: {str(e)}")
         
    def get_employee_by_id(self, employee_id: int) -> Employee:
        """Retrieve an employee by ID with related data"""
        employee = self.db.query(Employee).options(
            joinedload(Employee.user),
            joinedload(Employee.department),
            joinedload(Employee.position)
        ).filter(Employee.id == employee_id).first()
        if not employee:
            raise EmployeeNotFoundError(f"Employee with ID {employee_id} not found")
        return employee

    def get_all_employees(self, skip: int = 0, limit: Optional[int] = None) -> List[Employee]:
        """Retrieve all employees with optional pagination"""
        query = self.db.query(Employee).options(
            joinedload(Employee.user),
            joinedload(Employee.department),
            joinedload(Employee.position)
        ).offset(skip)
        if limit:
            query = query.limit(limit)
        employees = query.all()
        return employees

    def update_employee(self, employee_id: int, update_data: dict) -> Employee:
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
            
            self.db.commit()
            self.db.refresh(employee)
            return employee
        except SQLAlchemyError as e:
            self.db.rollback()
            raise EmployeeServiceError(f"Failed to update employee: {str(e)}")

    def delete_employee(self, employee_id: int) -> None:
        """Delete an employee and associated user"""
        employee = self.get_employee_by_id(employee_id)
        try:
            self.db.delete(employee)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise EmployeeServiceError(f"Failed to delete employee: {str(e)}")
        return None
