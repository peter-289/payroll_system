"""Routes that require admin privileges."""

from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from backend.database_setups.database_setup import get_db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, join

# Models
from backend.models.department_model import Department
from backend.models.Position_model import Position
from backend.models.employee_model import Employee
from backend.models.user_model import User

# Schemas

router = APIRouter(prefix="/api/admin", tags=["Admin Operations"])

# Department Management

@router.post("/departments/add")
def add_department(
    name: str = Form(...),
    description: str = Form(...),
    location: str = Form(None),
    salary_multiplier: float = Form(1.0),
    db: Session = Depends(get_db)
):
    """Admin route to add a new department."""
    existing = db.query(Department).filter(Department.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Department already exists.")

    new_department = Department(
        name=name,
        description=description,
        location=location,
        salary_multiplier=salary_multiplier
    )
    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return {"status": "success", "department": {"id": new_department.department_id, "name": new_department.name}}


@router.get("/departments/all")  
def get_all_departments(
    db: Session = Depends(get_db)
):
    """Admin route to get all departments."""
    departments = db.query(Department).all()
    department_list = [
        {
            "id": dept.department_id,
            "name": dept.name,
            "description": dept.description,
            "location": dept.location,
            "salary_multiplier": dept.salary_multiplier
        }
        for dept in departments
    ]
    return {"status": "success", "departments": department_list} 



# ----Delete Department ----
@router.delete("/departments/delete/{department_name}")
def delete_department(
    department_name: str,
    db: Session = Depends(get_db)
):
    """Admin route to delete a department."""
    department = db.query(Department).filter(Department.name == department_name).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found.")

    db.delete(department)
    db.commit()

    return {"status": "success", "message": f"Department {department_name} deleted."}


# ------Positions------
@router.post("/positions/add")
def add_positions(
    title : str = Form(...),
    department_name:str = Form(...),
    base_salary: float = Form(...),
    pay_grade: str = Form(...),
    db:Session = Depends(get_db)
    ):

    department_record = db.query(Department).filter(Department.name == department_name).first()
    if not department_record:
        raise HTTPException(status_code=404, detail=f"Department: {department_name} not found")
    
    exisiting_position = db.query(Position).filter(Position.title == title).first()
    if exisiting_position:
        raise HTTPException(status_code=400, detail=f"A position with name:{title} already exists!")
    
    department_id = department_record.department_id

    new_position = Position(
        title = title,
        department_id = department_id,
        base_salary = base_salary,
        pay_grade = pay_grade
    )
    try:
        db.add(new_position)
        db.commit()
        db.refresh(new_position)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    return {
        "detail":f"New position: {title} created successfully"
    }


# ---Get all Positions----
@router.get("/get-all-positions")
def get_all_positions(
    db:Session =Depends(get_db)
):
    
    positions = db.query(Position).all()
    position_list = [

        {  "title": position.title,
           "department_id": position.department_id,
           "base_salary": position.base_salary,
           "pay_grade": position.pay_grade,
         }
         for position in positions
    ]

    titles = [pos.title for pos in positions]

    return {
        "message":"success",
        "position_titles":titles
    }


# ----Remove positions-----
@router.delete("/delete-position")
def delete_position(
    position_name:str, 
    db:Session = Depends(get_db)
):
    position_record = db.query(Position).filter(Position.title == position_name).first()
    if not position_record:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Position {position_name} not found!")
    try:
        db.delete(position_record)
        db.commit()
    except SQLAlchemyError as e:
        return f"Error:{e}"
    return f"Position {position_name} deleted successfully!"



# ---------------------------------------------------------------------------------------
# ------------------- EMPLOYEE OPERATIONS -----------------------------------------------
# ---------------------------------------------------------------------------------------
@router.get("/get-all-employees")
def get_all_employees(db:Session = Depends(get_db)):
    employees = db.query(Employee).join(User).all()
    if not employees:
       raise HTTPException(404, f"No employees!")
    return employees


#-----------------------------------------------------------------------------------------
# -------------------- GET ALL USERS -----------------------------------------------------
@router.get("/get-all-users")
def get_all_users(db:Session = Depends(get_db)):
    users = db.query(User).all()
    return users





@router.get("/get-employee/{email}")
def get_employee(email:str, db:Session = Depends(get_db)):
    employee = db.query(User).join(Employee).filter(User.email == email).first()
    if not employee:
        raise HTTPException(404, f"employee with email:{email} not found!")
    
    return employee



#--------------------------------------------------------------------------
#       ----------- DELETE EMPLOYEE ---------------------------------------
#--------------------------------------------------------------------------
@router.delete("/delete-employee/{email}")
def delete_employee(email:str, db:Session = Depends(get_db)):
    employee = db.query(Employee).join(User).filter(User.email == email).first()
    if not employee:
        raise HTTPException(404,f"employee:{email} not found!")
    try:
        db.delete(employee)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(500, f"Could not complete operation:{e}")
    
    return {
        "message":f"Employee {employee.first_name} deleted successfully!"
    }


@router.delete("/delete-all-users")
def delete_all_users(db:Session = Depends(get_db)):
    
    try:
        deleted_count = db.query(User).delete()
        db.commit()
    except SQLAlchemyError as e:
        raise HTTPException(500, f"DB error:{e}")
    return {
        "message":f"Deleted all {deleted_count} users!"
    }