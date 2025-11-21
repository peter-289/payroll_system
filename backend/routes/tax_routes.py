from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from backend.dependancies.security import admin_access
from backend.schemas.tax_schema import TaxCreate, TaxResponse, TaxBracketCreate, TaxRuleUpdate, TaxBracketUpdate
from backend.database_setups.database_setup import get_db
from backend.utility_funcs.tax_bracket_validator import validate_no_overlaps
from backend.models.tax_model import TaxType, Tax
from backend.models.tax_brackets import TaxBracket




router = APIRouter(
    prefix="/tax", tags=["Tax"],
    dependencies=[Depends(admin_access)]
)



#======================================================================================================
#----------------------------- ADD TAX RULES  ----------------------------------------------------
@router.post("/add-tax-rule", dependencies=[Depends(admin_access)])
def add_tax_rule(payload: TaxCreate, db: Session = Depends(get_db)):
    if not payload.brackets or len(payload.brackets) == 0:
        raise HTTPException(status_code=400, detail="At least one tax bracket must be provided for tiered tax rules.")
    
    is_valid, error_message = validate_no_overlaps(payload.brackets)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)
    if payload.type not in [TaxType.PERCENTAGE, TaxType.FIXED, TaxType.TIERED]:
        raise HTTPException(status_code=400, detail="Invalid tax type. Must be 'percentage', 'fixed', or 'tiered'.")
    
    if payload.type == TaxType.TIERED and (not payload.brackets or len(payload.brackets) == 0):
        raise HTTPException(status_code=400, detail="Tiered tax rules must have at least one tax bracket.")
    if payload.type == TaxType.FIXED:
        raise HTTPException(status_code=400, detail="Fixed tax rules should not have tax brackets.")
    try:    
             new_tax_rule = Tax(
                 name=payload.name,
                 description=payload.description,
                 type=payload.type,
                 #fixed_amount=payload.fixed_amount,
                 effective_date=payload.effective_date,
                 expiry_date=payload.expiry_date
             )
    
             db.add(new_tax_rule)
             db.flush()  # To get the new_tax_rule.id
         
             for bracket in payload.brackets:
                 new_bracket = TaxBracket(
                     tax_id=new_tax_rule.id,
                     min_amount=bracket.min_amount,
                     max_amount=bracket.max_amount,
                     rate=bracket.rate,
                 
             )
                 db.add(new_bracket)
             db.commit()
             db.refresh(new_tax_rule)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add tax rule: {e}")
    
    return {"message": f"Tax rule added successfully!:{new_tax_rule.name}"}


#======================================================================================================
#-------------------------------- PATCH TAX RULES METADATA -----------------------------------------------------
@router.patch("/update-tax-rule/{rule_id}", response_model=TaxResponse)
def update_tax_rule(
    rule_id: int,
    data: TaxRuleUpdate,
    db: Session = Depends(get_db),
):
    rule = db.query(Tax).filter(Tax.id == rule_id).first()

    if not rule:
        raise HTTPException(404, "Tax rule not found")
    

    updated_fields = Tax(
        name=data.name or rule.name,
        description=data.description or rule.description,
        type=data.type or rule.type,
        #fixed_amount=data.fixed_amount or rule.fixed_amount,
        effective_date=data.effective_date or rule.effective_date,
        expiry_date=data.expiry_date or rule.expiry_date,
    )
    
    for key, value in updated_fields.__dict__.items():
        if key != "_sa_instance_state" and value is not None:
            setattr(rule, key, value)
    db.commit()
    db.refresh(rule)

    return rule

#======================================================================================================
#---------------------------- UPDATE TAX BRACKETS ------------------------------------------------------
@router.put("/update-tax-brackets/{rule_id}", response_model=TaxResponse)
def update_tax_brackets(
    rule_id: int,
    brackets:list[TaxBracketUpdate],
    db: Session = Depends(get_db),
):
    rule = db.query(Tax).filter(Tax.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Tax rule not found")
    
    is_valid, error_message = validate_no_overlaps(brackets)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)

    try:
        # Delete existing brackets
        db.query(TaxBracket).filter(TaxBracket.tax_id == rule_id).delete()

        # Add new brackets
        for bracket in brackets:
            new_bracket = TaxBracket(
                tax_id=rule_id,
                min_amount=bracket.min_amount,
                max_amount=bracket.max_amount,
                rate=bracket.rate,
            )
            db.add(new_bracket)

        db.commit()
        db.refresh(rule)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update tax brackets: {e}")

    return rule

#======================================================================================================
#---------------------------- GET TAX RULE BY ID ------------------------------------------------------
@router.get("/get-tax-rule/{rule_id}", response_model=TaxResponse)
def get_tax_rule(rule_id:int, db:Session = Depends(get_db)):
    rule = (
        db.query(Tax)
        .filter(Tax.id == rule_id).first()
    )
    if not rule:
        raise HTTPException(status_code=404, detail=f"Rule not found!:{rule_id}")
    return rule


#=======================================================================================================
#-------------------------------- GET ALL TAX RULES ----------------------------------------------------
@router.get("/get-all-tax-rules", response_model=list[TaxResponse])
def get_tax_rules(db:Session = Depends(get_db)):
    rules = (
        db.query(Tax)
        .order_by(Tax.created_at.desc()).all()
        )
    if not rules:
        raise HTTPException(status_code=404, detail="No rules found!")
    return rules


#=======================================================================================================
#-------------------------------- DELETE TAX RULES -----------------------------------------------------
@router.delete("/delete-tax-rule/{name}")
def delete_tax_rule(name:str, db:Session =Depends(get_db)):
    tax_rule = db.query(Tax).filter(Tax.name == name).first()
    if not tax_rule:
        raise HTTPException(status_code=404, detail=f"Tax-rule:{name} not found!")
    try:
        db.delete(tax_rule)
        db.commit()
    except:
        return{"detail":f"Could not remove tax-rule: {tax_rule.name} from db!"}
    
    return {"message":f"Successfully removed tax rule:{tax_rule.name} from db!"}