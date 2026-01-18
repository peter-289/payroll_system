from sqlalchemy.orm import Session
from app.models.allowances_model import Allowance, AllowanceType
from typing import Optional, List
from app.domain.enums import AllowanceStatus


class AllowanceRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_allowance(self, allowance: Allowance) -> Allowance:
        self.db.add(allowance)
        self.db.commit()
        self.db.refresh(allowance)
        return allowance


    def update_allowance(self, allowance: Allowance) -> Allowance:
        self.db.commit()
        self.db.refresh(allowance)
        return allowance
    

    def get_allowance_by_id(self, allowance_id: int) -> Optional[Allowance]:
        return self.db.query(Allowance).filter(Allowance.id == allowance_id).first()
    

    def get_allowance_by_type(self,allowance_type_id: int) -> Optional[Allowance]:
        return self.db.query(Allowance).filter(
            Allowance.allowance_type_id == allowance_type_id
        ).first()


    def get_allowances_by_payroll(self, payroll_id: int) -> List[Allowance]:
        return self.db.query(Allowance).filter(Allowance.payroll_id == payroll_id).all()

    def get_all_allowances(self) -> List[Allowance]:
        return self.db.query(Allowance).all()

    def get_allowances_by_type(self, allowance_type_id: int) -> List[Allowance]:
        return self.db.query(Allowance).filter(Allowance.allowance_type_id == allowance_type_id).all()

    def delete_allowance(self, allowance: Allowance) -> None:
        self.db.delete(allowance)
        self.db.commit()


# ============================================================================================
# ------------------ ALLOWANCE TYPE METHODS --------------------------------------------------
    def save_allowance_type(self, allowance_type: AllowanceType) -> AllowanceType:
        self.db.add(allowance_type)
        self.db.commit()
        self.db.refresh(allowance_type)
        return allowance_type
    
    def roll_back(self):
        self.db.rollback()

    def update_allowance_type(self, allowance_type: AllowanceType) -> AllowanceType:
        self.db.commit()
        self.db.refresh(allowance_type)
        return allowance_type

    def get_allowance_type_by_id(self, id: int) -> Optional[AllowanceType]:
        return self.db.query(AllowanceType).filter(AllowanceType.id == id).first()

    def get_allowance_type_by_code(self, code: str, name: str) -> Optional[AllowanceType]:
        return self.db.query(AllowanceType).filter(AllowanceType.code == code, AllowanceType.name == name).first()

    def get_all_allowance_types(self, active_only: bool = True) -> List[AllowanceType]:
        query = self.db.query(AllowanceType)
        if active_only:
            query = query.filter(AllowanceType.status == AllowanceStatus.ACTIVE)
        return query.all()

    def delete_allowance_type(self, allowance_type: AllowanceType) -> None:
        self.db.delete(allowance_type)
        self.db.commit()
    
    
