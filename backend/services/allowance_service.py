from fastapi import HTTPException, status
from backend.schemas.allowance_schema import AllowanceCreate
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from backend.models.allowances_model import Allowance
from datetime import datetime
from backend.services.allowance_type_service import AllowanceTypeService
from backend.services.insuarance_service import InsuranceService
from backend.models.allowances_model import AllowanceStatus
import random
from decimal import Decimal, InvalidOperation


class AllowanceService:
    def __init__(self, db:Session):
        self.db = db
    
    def _generate_reference_number(self) -> str:
        """Generates a unique reference number for the allowance."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        rand = random.randint(1000, 9999)
        return f"ALW-{timestamp}-{rand}"
    
    def _check_existing_allowance(self, payroll_id:int, allowance_type_id:int):
        existing_allowance = self.db.query(Allowance).filter_by(
            payroll_id=payroll_id,
            allowance_type_id=allowance_type_id
        ).first()
        if existing_allowance:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Allowance of type ID {allowance_type_id} already exists for payroll ID {payroll_id}."
            )
        return None
    
    def _validate_allowance_input(self, payload, allowance_type):
          """Validates allowance input before creating the allowance record."""
        
        # 1. Validate amount is a valid decimal
          try:
            amount = Decimal(payload.amount)
          except (InvalidOperation, TypeError):
            raise HTTPException(
                status_code=400,
                detail="Amount must be a valid decimal number."
            )

        # 2. Amount must be non-negative
          if amount < 0:
            raise HTTPException(
                status_code=400,
                detail="Amount cannot be negative."
            )

        # 3. Enforce min/max limits if defined
          if allowance_type.min_amount is not None and amount < allowance_type.min_amount:
            raise HTTPException(
                status_code=400,
                detail=f"Amount must be >= minimum {allowance_type.min_amount}."
            )

          if allowance_type.max_amount is not None and amount > allowance_type.max_amount:
            raise HTTPException(
                status_code=400,
                detail=f"Amount must be <= maximum {allowance_type.max_amount}."
            )

        # 4. Percentage-based allowances must have a basis
          if allowance_type.is_percentage_based:
            if not payload.calculation_basis:
                raise HTTPException(
                    status_code=400,
                    detail="Percentage-based allowances must specify calculation_basis."
                )

        # 5. Fixed allowances should not send percentage basis unless necessary
          if not allowance_type.is_percentage_based and payload.calculation_basis:
            raise HTTPException(
                status_code=400,
                detail="calculation_basis should only be used for percentage-based allowances."
            )
          return True
    
    def create_allowance(self, payload:AllowanceCreate):
        self._check_existing_allowance(payload.payroll_id, payload.allowance_type_id)
        service = AllowanceTypeService(self.db)
        allowance_type = service.get_allowance_type(payload.allowance_type_id)
        self._validate_allowance_input(payload, allowance_type)

        new_allowance = Allowance(
            payroll_id=payload.payroll_id,
            allowance_type_id=payload.allowance_type_id,
            name=allowance_type.name,
            code=allowance_type.code,
            amount=payload.amount,
            description=payload.description or allowance_type.description,
            is_taxable=allowance_type.is_taxable,
            calculation_basis=payload.calculation_basis,
            status=AllowanceStatus.ACTIVE,
            reference_number=payload.Reference_number or self._generate_reference_number(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        try:
            self.db.add(new_allowance)
            self.db.commit()
            self.db.refresh(new_allowance)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create new allowance{e}")

        return new_allowance
        
    
    def get_allowances(self):
        allowances = self.db.query(Allowance).all()
        return allowances
    
    def get_allowance(self, allowance_id:int):
        allowance = self.db.get(Allowance, allowance_id)
        if not allowance:
            raise HTTPException(status_code=404, detail=f"No allowance with id:{allowance_id} not found!")
        return allowance
    
    def delete_allowance(self, allowance_id:int):
        allowance = self.db.get(Allowance, allowance_id)
        if not allowance:
            raise HTTPException(status_code=404, detail=f"Allowance with id {allowance_id} could not be found!")
        try:
            self.db.delete(allowance)
            self.db.commit()
            return {"message":f"Allowance with id:{allowance_id} deleted successfuly!"}
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Could not delete allowance:{e}")
