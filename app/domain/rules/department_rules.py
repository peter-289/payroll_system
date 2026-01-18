from app.domain.exceptions.base import DepartmentServiceError


def ensure_no_duplicate_department(existing_department, department_name: str):
    """Ensure no duplicate department exists with the same name."""
    if existing_department:
        raise DepartmentServiceError(f"Department with name '{department_name}' already exists")
