from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.core.security import admin_access
from app.schemas.tax_schema import TaxCreate, TaxResponse, TaxBracketCreate, TaxRuleUpdate, TaxBracketUpdate
from app.db.database_setup import get_db
from app.services.tax_service import TaxService
from app.domain.exceptions.base import TaxServiceError, TaxRuleNotFoundError, InvalidTaxBracketsError




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
    try:
        tax_service = TaxService(db)
        new_tax_rule = tax_service.create_tax_rule(data)
        return new_tax_rule
    except InvalidTaxBracketsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except TaxServiceError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


#======================================================================================================
#-------------------------------- PATCH TAX RULES METADATA -----------------------------------------------------
@router.patch("/taxes/{rule_id}", response_model=TaxResponse, status_code=200)
def update_tax_rule(
    rule_id: int,
    payload: TaxRuleUpdate,
    db: Session = Depends(get_db),
):
    try:
        service = TaxService(db)
        tax_rule = service.update_tax_rule(rule_id, payload)
        return tax_rule
    except TaxRuleNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TaxServiceError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

#======================================================================================================
#---------------------------- UPDATE TAX BRACKETS ------------------------------------------------------
@router.put("/taxes/{rule_id}", response_model=TaxResponse, status_code=200)
def update_tax_brackets(
    rule_id: int,
    brackets:list[TaxBracketUpdate],
    db: Session = Depends(get_db),
):
    try:
        service = TaxService(db)
        tax_rule = service.update_tax_brackets(rule_id, brackets)
        return tax_rule
    except TaxRuleNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidTaxBracketsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except TaxServiceError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

#======================================================================================================
#---------------------------- GET TAX RULE BY ID ------------------------------------------------------
@router.get("/taxes/{rule_id}", response_model=TaxResponse, status_code=200)
def get_tax_rule(rule_id:int, db:Session = Depends(get_db)):
    try:
        service = TaxService(db)
        tax_rule = service.get_tax_rule(rule_id)
        return tax_rule
    except TaxRuleNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


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
    try:
        service = TaxService(db)
        service.delete_tax_rule(taxes_id)
        return None
    except TaxRuleNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TaxServiceError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))