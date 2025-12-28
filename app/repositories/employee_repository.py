from sqlalchemy.orm import Session
from app.models.employee_model import Employee


class EmployeeRepository:
    """Repository that encapsulates DB access for Employee objects.

    Responsibilities:
    - Purely data access. No business rules.
    - Return ORM objects or None.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, employee_id: int) -> Employee | None:
        if employee_id <= 0:
            return None
        return self.db.query(Employee).filter(Employee.id == employee_id).first()
