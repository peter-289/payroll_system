from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from backend.dependancies.security import admin_access
from backend.schemas.tax_schema import TaxCreate, TaxResponse, TaxBracketCreate, TaxRuleUpdate, TaxBracketUpdate
from backend.database_setups.database_setup import get_db
from backend.utility_funcs.tax_bracket_validator import validate_no_overlaps
from backend.models.tax_model import TaxType, Tax
from backend.models.tax_brackets import TaxBracket
from backend.services.tax_service import TaxService




router = APIRouter(
    prefix="/api/v1", tags=["Taxes"],
    
)



#======================================================================================================
#----------------------------- ADD TAX RULES  ----------------------------------------------------
@router.post("/taxes", status_code=status.HTTP_201_CREATED, response_model=TaxResponse)
def add_tax_rule(
    data: TaxCreate,
    db: Session = Depends(get_db),
):
    tax_service = TaxService(db)
    new_tax_rule = tax_service.create_tax_rule(data)
    return new_tax_rule


#======================================================================================================
#-------------------------------- PATCH TAX RULES METADATA -----------------------------------------------------
@router.patch("/taxes/{rule_id}", response_model=TaxResponse, status_code=200)
def update_tax_rule(
    rule_id: int,
    db: Session = Depends(get_db),
):
    service = TaxService(db)
    tax_rule = service.update_tax_rule(rule_id)
    return tax_rule

#======================================================================================================
#---------------------------- UPDATE TAX BRACKETS ------------------------------------------------------
@router.put("/taxes/{rule_id}", response_model=TaxResponse, status_code=200)
def update_tax_brackets(
    rule_id: int,
    brackets:list[TaxBracketUpdate],
    db: Session = Depends(get_db),
):
    service = TaxService(db)
    tax_rule = service.update_tax_brackets(rule_id, brackets)
    return tax_rule

#======================================================================================================
#---------------------------- GET TAX RULE BY ID ------------------------------------------------------
@router.get("/taxes/{rule_id}", response_model=TaxResponse, status_code=200)
def get_tax_rule(rule_id:int, db:Session = Depends(get_db)):
    service = TaxService(db)
    tax_rule = service.get_tax_rule(rule_id)
    return tax_rule


#=======================================================================================================
#-------------------------------- GET ALL TAX RULES ----------------------------------------------------
@router.get("/taxes", response_model=list[TaxResponse], status_code=200)
def get_tax_rules(db:Session = Depends(get_db)):
    tax_rules = TaxService(db).list_tax_rules()  
    return tax_rules

#=======================================================================================================
#-------------------------------- DELETE TAX RULES -----------------------------------------------------
@router.delete("/taxes/{tax_id}", status_code=204)
def delete_tax_rule(taxes_id:int, db:Session =Depends(get_db)):
    service = TaxService(db)
    service.delete_tax_rule(taxes_id)
    return None