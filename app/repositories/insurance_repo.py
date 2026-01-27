from app.models.insurance_model import Insurance
from sqlalchemy.orm import Session
from typing import Optional

class InsuranceRepository:
    def __init__(self, db:Session):
        self.db = db

    def get_insurance_by_policy_number(self, policy_number:str)->Optional[Insurance]:
        return self.db.query(Insurance).filter(Insurance.policy_number == policy_number).first()