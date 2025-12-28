from datetime import date
from sqlalchemy.orm import Session
from app.models.salary_model import PositionSalary


class PositionSalaryRepository:
    """Repository for position-level salaries."""

    def __init__(self, db: Session):
        self.db = db

    def get_active(self, position_id: int, as_of_date: date) -> PositionSalary | None:
        if position_id <= 0:
            return None
        q = (
            self.db.query(PositionSalary)
            .filter(PositionSalary.position_id == position_id)
            .filter(PositionSalary.effective_from <= as_of_date)
            .filter((PositionSalary.effective_to == None) | (PositionSalary.effective_to >= as_of_date))
            .order_by(PositionSalary.effective_from.desc())
        )
        return q.first()
