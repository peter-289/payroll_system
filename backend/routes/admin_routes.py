from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from backend.database_setups.database_setup import get_db
from backend.dependancies.security import  admin_access, hash_password, parse_date, create_temporary_password
from backend.models.user_model import User
from backend.models.employee_model import Employee
from backend.models.roles_model import Role
from backend.models.Position_model import Position
from backend.models.department_model import Department
from backend.models.employee_bank_account import EmployeeBankAccount
from backend.models.employee_contacts_details import EmployeeContact
from backend.schemas.employee_schema import EmployeeCreateSchema, EmployeeResponseSchema

router = APIRouter(
    prefix="/admin", tags=["Admin"]
)


#======================================================================================================
#----------------------------- CREATE EMPLOYEE ------------------------------------------------------
#======================================================================================================
@router.post("/create_employee", status_code=status.HTTP_201_CREATED, dependencies=[Depends(admin_access)])
def create_employee(
    employee: EmployeeCreateSchema,
    db: Session = Depends(get_db),
):
    form = employee.dict()
    
    existing_user = db.query(User).filter(User.username == form["username"]).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    role = db.query(Role).filter(Role.role_name == form["role_name"]).first()
    if not role:
        raise HTTPException(status_code=400, detail="Role does not exist")
    pass_ = create_temporary_password()
    hashed_password = hash_password(pass_)
    try:
       new_user = User(
            first_name=form["first_name"],
            last_name=form["last_name"],
            username=form["username"],
            password_hash=hashed_password,
            role_id=role.id
     )
       db.add(new_user)
       db.flush()
       
    
       # Find department by name
       department = db.query(Department).filter(Department.name == form["department_name"]).first()
       if not department:
           raise HTTPException(status_code=400, detail=f"Department '{form['department_name']}' does not exist")
       
       # Find position by title in the selected department
       position = db.query(Position).filter(
           Position.title == form["position_title"],
           Position.department_id == department.id
       ).first()
       if not position:
           raise HTTPException(
               status_code=400, 
               detail=f"Position '{form['position_title']}' does not exist in department '{form['department_name']}'"
           )
       
       date_of_birth = parse_date(form["date_of_birth"])
       new_employee = Employee(
           user_id=new_user.id,
           first_name=form["first_name"],
           last_name=form["last_name"],
           date_of_birth=date_of_birth,
           employment_status="Active",
           salary_type="Monthly",
           department_id=department.id,
           position_id=position.id
        )

       db.add(new_employee)
       db.flush()
       
        
       existing_contact = db.query(EmployeeContact).filter(EmployeeContact.phone == form["phone_number"]).first()
       if existing_contact:
            raise HTTPException(status_code=400, detail="Phone number already exists")
       contact_details = EmployeeContact(
           employee_id=new_employee.id,
           email=form["email"],
           phone=form["phone_number"],
           address=form["address"],
           city=form["city"],
           country=form["country"]
       )
       db.add(contact_details)
       
       existing_bank_account = db.query(EmployeeBankAccount).filter(EmployeeBankAccount.account_number == form["account_number"]).first()
       if existing_bank_account:
            raise HTTPException(status_code=400, detail="Bank account number already exists")
       bank_account = EmployeeBankAccount(
           employee_id=new_employee.id,
           bank_name=form["bank_name"],
           account_number=form["account_number"],
           account_type=form["account_type"]
       )
       db.add(bank_account)
    
       db.commit()
       db.refresh(new_employee)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create employee: {e}" )
    
    return {"message": "Employee created successfully", "user_id": new_user.id
            , "temporary_password": pass_}


#======================================================================================================
#----------------------------- GET ALL DEPARTMENTS -------------------------------------------------
@router.get("/departments-all", dependencies=[Depends(admin_access)])
def get_all_departments(
    db: Session = Depends(get_db),
    #admin_user: User = Depends(check_admin_access)
):
    departments = db.query(Department).all()
    return [{"id": dept.id, "name": dept.name} for dept in departments]

@router.get("/positions-by-department/{department_name}")
def get_positions_by_department(
    department_name: str,
    db: Session = Depends(get_db),
    #admin_user: User = Depends(check_admin_access)
):
    department = db.query(Department).filter(Department.name == department_name).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    positions = db.query(Position).filter(Position.department_id == department.id).all()
    return [{"id": pos.id, "title": pos.title} for pos in positions]