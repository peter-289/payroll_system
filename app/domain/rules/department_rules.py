from app.domain.exceptions.base import  DepartmentAlreadyExistsError


def ensure_no_duplicate_department(existing_department, department_name: str):
    """Ensure no duplicate department exists with the same name."""
    if existing_department:
        raise DepartmentAlreadyExistsError (f"Department with name '{department_name}' already exists")
