from sqlalchemy.orm import Session
from backend.schemas.insurance_schema import InsuranceCreate, InsuranceResponse
from backend.models.Insuarance_model import Insurance
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime



class InsuranceService:
    def __init__(self, db:Session):
        self.db = db
    
    def _generate_policy_number(self) -> str:
        import uuid
        return "POL-" + uuid.uuid4().hex[:10].upper()    

    
    def create_insurance(self, data: InsuranceCreate):
        # Ensure policy number doesn’t duplicate
        policy_number = self._generate_policy_number()
        print(policy_number)
        existing = self.db.query(Insurance).filter(
            Insurance.policy_number == policy_number
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Policy number already exists!"
            )

        insurance_id = Insurance(
            employee_id=data.employee_id,
            insurance_provider=data.insurance_provider,
            policy_number=policy_number,
            coverage_type=data.coverage_type,
            premium_amount=data.premium_amount,
            employer_contribution=data.employer_contribution,
            employee_contribution=data.employee_contribution,
            start_date=data.start_date,
            end_date=data.end_date,
            status=data.status
        )
        try:
            self.db.add(insurance_id)
            self.db.commit()
            self.db.refresh(insurance_id)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Could not create an insuarance:{e}!")
           
        return insurance_id
    
    def get_policy(self, insurance_id:int):
        policy = self.db.query(Insurance).filter(Insurance.id == insurance_id).first()
        if not policy:
            raise HTTPException(status_code=404, detail=f"Could not find policy with id:{insurance_id}!")
        return policy
    
    def get_all_policies(self):
        return self.db.query(Insurance).all()
    
    def soft_delete_policy(self, insurance_id: int):
       policy = self.db.get(Insurance, insurance_id)

       if not policy:
           raise HTTPException(status_code=404, detail="Policy not found!")
       try:
            policy.status = "cancelled"
            policy.end_date = datetime.utcnow()
            self.db.commit()
       except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Policy could not be cancelled!")
       return {"message": "Policy cancelled successfully"}

    def delete_policy(self, insurance_id:int):
        policy = self.db.query(Insurance).filter(Insurance.id == insurance_id).first()
        if not policy:
            raise HTTPException(status_code=404, detail=f"Policy with id:{insurance_id} not found!")
        try:
            self.db.delete(policy)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Could not delete policy!")
        return {"message":f"Policy with id {insurance_id} deleted successfuly!"}

    

