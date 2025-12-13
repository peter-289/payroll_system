from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from backend.schemas.tax_schema import TaxBracketCreate, TaxBracketUpdate, TaxCreate
from backend.database_setups.database_setup import get_db
from backend.utility_funcs.tax_bracket_validator import validate_no_overlaps
from backend.models.tax_model import TaxType, Tax
from backend.models.tax_brackets import TaxBracket
from datetime import datetime


class TaxService:
    def __init__(self, db:Session):
        self.db = db
    
    def _generate_tax_code(self, payload:TaxCreate):
        prefix = payload.name[:3].upper()
        unique_code = f"{prefix}-{int(datetime.utcnow().timestamp())}"
        return unique_code

        

    def _validate_payload(self, payload:TaxCreate):
        valid, error = validate_no_overlaps(payload.brackets)
        if payload.type == TaxType.TIERED and len(payload.brackets)==0:
            raise HTTPException(status_code=400, detail="Atleast one bracket required for tiered taxes!")
        if not valid:
            raise HTTPException(status_code=400, detail=error)
        if payload.type not in [TaxType.FIXED, TaxType.GRADUATED, TaxType.PERCENTAGE, TaxType.TIERED]:
            raise HTTPException(status_code=400, detail="Invalid tax type!: accepted values; fixed, graduated, tiered, percentage ")
        if payload.type == TaxType.FIXED:
           raise HTTPException(status_code=400, detail="Fixed tax rules should not have tax brackets.")
        return True
    
    def create_tax_rule(self, payload:TaxCreate,):
        code = self._generate_tax_code(payload)
        self._validate_payload(payload)
        new_tax_rule = Tax(
            tax_code=code,
            name=payload.name,
            description=payload.description,
            tax_type=payload.type,
            effective_date=payload.effective_date,
            expiry_date=payload.expiry_date
        )
        try:

          self.db.add(new_tax_rule)
          self.db.flush()  # To get the new_tax_rule.id
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating tax rule: {str(e)}")
        for bracket in payload.brackets:
            new_bracket = TaxBracket(
                tax_id=new_tax_rule.id,
                min_amount=bracket.min_amount,
                max_amount=bracket.max_amount,
                rate=bracket.rate,
            )
            self.db.add(new_bracket)
        try:
         self.db.commit()
         self.db.refresh(new_tax_rule)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to add tax rule: {e}")
        return new_tax_rule
    
    def get_tax_rule(self, tax_id:int):
        tax_rule = self.db.query(Tax).filter(Tax.id == tax_id).first()
        if not tax_rule:
            raise HTTPException(status_code=404, detail="Tax rule not found.")
        return tax_rule
    
    def update_tax_rule(self, tax_id:int, payload:TaxCreate):
        tax_rule = self.get_tax_rule(tax_id)
        self._validate_payload(payload)
        
        tax_rule.name = payload.name
        tax_rule.description = payload.description
        tax_rule.tax_type = payload.type
        tax_rule.effective_date = payload.effective_date
        tax_rule.expiry_date = payload.expiry_date
        
        try:
            self.db.commit()
            self.db.refresh(tax_rule)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to update tax rule: {e}")
        
        return tax_rule
    
    def update_tax_brackets(self, tax_id:int, brackets:list[TaxBracketCreate]):
        tax_rule = self.get_tax_rule(tax_id)
        is_valid, error_message = validate_no_overlaps(brackets)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_message)

        try:
            # Delete existing brackets
            self.db.query(TaxBracket).filter(TaxBracket.tax_id == tax_id).delete()

            # Add new brackets
            for bracket in brackets:
                new_bracket = TaxBracket(
                    tax_id=tax_id,
                    min_amount=bracket.min_amount,
                    max_amount=bracket.max_amount,
                    rate=bracket.rate,
                )
                self.db.add(new_bracket)

            self.db.commit()
            self.db.refresh(tax_rule)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to update tax brackets: {e}")

        return tax_rule
    
    def delete_tax_rule(self, tax_id:int):
        tax_rule = self.get_tax_rule(tax_id)
        try:
            self.db.delete(tax_rule)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to delete tax rule: {e}")
        return {"message": "Tax rule deleted successfully."}
    
    def list_tax_rules(self, skip:int=0, limit:int=100):
        tax_rules = self.db.query(Tax).offset(skip).limit(limit).all()
        return tax_rules