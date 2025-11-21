from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database_setups.database_setup import get_db
from backend.dependancies.security import  admin_access
from backend.models.Position_model import Position
from backend.models.department_model import Department


router = APIRouter(prefix="/api",
                 tags=["Departments"],
                 dependencies=[Depends(admin_access)]
                   )



#======================================================================================================
#----------------------------- GET ALL DEPARTMENTS -------------------------------------------------
@router.get("/departments-all")
def get_all_departments(
    db: Session = Depends(get_db),
    #admin_user: User = Depends(check_admin_access)
):
    departments = db.query(Department).all()
    return [{"id": dept.id, "name": dept.name} for dept in departments]



#======================================================================================================
#----------------------------- GET POSITIONS BY DEPARTMENT ------------------------------------------
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


