from sqlalchemy.orm import Session
from app.models.roles_model import Role
from app.models.permissions_model import Permissions
from app.models.role_permission import RolePermission
from app.models.department_model import Department
from app.models.Position_model import Position
from fastapi import HTTPException, status
from app.db.database_setup import SessionLocal
from app.services.salary_service import SalaryService
from app.models.salary_model import PositionSalary, PayFrequency
from datetime import date


# ---- Seed roles ---- #
def seed_roles(db:Session):
    roles = [
        {"role_name": "admin", "description": "System Administrator"},
        {"role_name": "hr", "description": "Human Resources Manager"},
        {"role_name": "employee", "description": "Regular employee role"},
    ]
    for role_data in roles:
        existing_role = db.query(Role).filter_by(role_name=role_data["role_name"]).first()
        if not existing_role:
            new_role = Role(**role_data)
            db.add(new_role)

            print(f"Added role: {role_data['role_name']}, description: {role_data['description']}")
        else:
            print(f"Role already exists: {role_data['role_name']}, description: {role_data['description']}")
    db.commit()



# ---- Seed permissions ---- #
def seed_permissions(db:Session):
    permissions = [
        {"permission_name": "view_payroll", "description": "Can view payroll information"},
        {"permission_name": "edit_payroll", "description": "Can edit payroll information"},
        {"permission_name": "delete_payroll", "description": "Can delete payroll records"},
        {"permission_name": "view_users", "description": "Can view user accounts"},
        {"permission_name": "add_users", "description": "Can add user accounts"},
        {"permission_name": "delete_users", "description": "Can delete user accounts"},
        {"permission_name": "manage_roles", "description": "Can manage roles and permissions"},
        {"permission_name": "view_reports", "description": "Can view system reports"},
        {"permission_name": "edit_reports", "description": "Can edit system reports"},
        {"permission_name": "delete_reports", "description": "Can delete system reports"},
    ]
    for perm_data in permissions:
        existing_perm = db.query(Permissions).filter_by(permission_name=perm_data["permission_name"]).first()
        if not existing_perm:
            new_perm = Permissions(**perm_data)
            db.add(new_perm)

            print(f"Added permission: {perm_data['permission_name']}, description: {perm_data['description']}")
        else:
            print(f"Permission already exists: {perm_data['permission_name']}, description: {perm_data['description']}")
    db.commit()



# ----- Seed roles and permissions ---- #

def seed_role_permissions(db: Session):
    role_perm_map = {
        "admin": ["view_users", "delete_users"],
        "hr": ["view_users"],
        "employee": ["view_users"]
    }

    for role_name, perm_names in role_perm_map.items():
        role = db.query(Role).filter_by(role_name=role_name).first()
        if not role:
            print(f"Role '{role_name}' not found, skipping.")
            continue

        for perm_name in perm_names:
            perm = db.query(Permissions).filter_by(permission_name=perm_name).first()
            if not perm:
                print(f"Permission '{perm_name}' not found, skipping assignment for role '{role_name}'.")
                continue

            # Avoid duplicate entries in join table
            exists = db.query(RolePermission).filter_by(
                role_id=role.id,
                permission_id=perm.id
            ).first()
            if exists:
                print(f"Role '{role_name}' already has permission '{perm_name}', skipping.")
                continue

            db.add(RolePermission(role_id=role.id, permission_id=perm.id))
            print(f"Assigned permission '{perm_name}' to role '{role_name}'")

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        # raise the underlying exception — don't import FastAPI exceptions in seed scripts
        raise RuntimeError(f"Failed to seed role_permissions: {e}") from e




# ---Seed departments -----#
def seed_departments(db: Session):
    
    departments = [
        {"name": "Human Resources", "description": "Handles hiring, onboarding, and employee welfare.", "location": "Nairobi"},
        {"name": "Engineering", "description": "Responsible for product development and maintenance.", "location": "Nairobi"},
        {"name": "Finance", "description": "Manages payroll, budgets, and expenditures.", "location": "Nairobi"},
        {"name": "Marketing", "description": "Handles branding, advertising, and outreach.", "location": "Nairobi"},
        {"name": "Operations", "description": "Oversees daily business operations.", "location": "Nairobi"},
        {"name": "Sales", "description": "Handles sales", "location":"Nairobi"}
    ]

    for dept_data in departments:
        existing = db.query(Department).filter(Department.name == dept_data["name"]).first()
        if not existing:
            db.add(Department(**dept_data))
            print(f"✅ Added department: {dept_data['name']}")
        else:
            print(f"⚠️ Department already exists: {dept_data['name']}")
    db.commit()
    db.close()

# -----Seed positions---
def seed_positions(db: Session):
    departments = {
        "Engineering": db.query(Department).filter_by(name="Engineering").first(),
        "HR": db.query(Department).filter_by(name="Human Resources").first(),
        "Finance": db.query(Department).filter_by(name="Finance").first(),
        "Operations": db.query(Department).filter_by(name ="Operations").first(),
        "Sales": db.query(Department).filter_by(name="Sales").first(),

    }

    positions_data = [
        {"title": "Software Engineer",  "department": departments["Engineering"]},
        {"title": "QA Analyst",  "department": departments["Engineering"]},
        {"title": "HR Officer",  "department": departments["HR"]},
        {"title": "Accountant",  "department": departments["Finance"]},
        {"title": "Sales Representative",  "department": departments["Sales"]},
    ]

    for pos in positions_data:
        position = db.query(Position).filter_by(title = pos["title"]).first()
        if not position:
            new_pos = Position(
                title=pos["title"],
                department_id=pos["department"].id
            )
            db.add(new_pos)
            print(f"[OK]Added position:{pos['title']}")
        else:
            print(f"[OK]Position already exists:{pos['title']}")
    db.commit()
    print("[OK] Positions seeded successfully.")

#========================================================================================
# Seed salaries
def seed_salaries(db: Session):
    repo = SalaryService(db)
    today = date.today()
    salaries= [
        {"position_id": 1, "amount": 8000.0, "salary_type": PayFrequency.MONTHLY},
        {"position_id": 2, "amount": 6000.0, "salary_type": PayFrequency.MONTHLY},
        {"position_id": 3, "amount": 5000.0, "salary_type": PayFrequency.MONTHLY},
        {"position_id": 4, "amount": 7000.0, "salary_type": PayFrequency.MONTHLY},
        {"position_id": 5, "amount": 4000.0, "salary_type": PayFrequency.MONTHLY},
    ]
    inserted_count = 0
    skipped_count = 0
    try:
        for item in salaries:
            existing = repo.get_position_salaries(item["position_id"])
            if existing:
                print(f"[*]Salary for position_id {item['position_id']} already exists. Skipping.")
                skipped_count += 1
                continue
            else:
                repo.add_position_salary(
                    position_id=item["position_id"],
                    amount=item["amount"],
                    salary_type=item["salary_type"],
                    effective_from=today,   
                    created_by=1
                )
                print(f"[*]Added {inserted_count} ssalries and skipped {skipped_count} salaries.")
                inserted_count += 1
            

    except Exception as e:
        raise RuntimeError(f"[*]Failed to seed salaries: {e}") from e
        
        