from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.tax_brackets_service import TaxBracketsService
from app.db.database_setup import get_db
from app.schemas.tax_brackets_schema import TaxBracketCreate, TaxBracketUpdate, TaxBracketResponse
from app.core.security import admin_access
from app.repositories.tax_brackets_repo import TaxBracketsRepository
from typing import List

router = APIRouter(prefix="/api/v1", tags=["Tax Brackets"])


@router.post("/tax-brackets", response_model=TaxBracketResponse, status_code=status.HTTP_201_CREATED)
def create_tax_bracket(
    payload: TaxBracketCreate,
    db: Session = Depends(get_db),
    _: None = Depends(admin_access)
):
    """Create a new tax bracket."""
    repo = TaxBracketsRepository(db)
    service = TaxBracketsService(repo)

    try:
        tax_bracket = service.create_bracket(
            tax_id=payload.tax_id,
            min_amount=payload.min_amount,
            max_amount=payload.max_amount,
            rate=payload.rate,
            description=payload.description,
            deductible_amount=payload.deductible_amount,
            effective_from=payload.effective_from,
            effective_to=payload.effective_to
        )
        return tax_bracket
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create tax bracket: {str(e)}"
        )


@router.get("/tax-brackets/{tax_bracket_id}", response_model=TaxBracketResponse)
def get_tax_bracket(
    tax_bracket_id: int,
    db: Session = Depends(get_db)
):
    """Get a tax bracket by ID."""
    repo = TaxBracketsRepository(db)
    service = TaxBracketsService(repo)

    tax_bracket = service.get_bracket_by_id(tax_bracket_id)
    if not tax_bracket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tax bracket not found"
        )
    return tax_bracket


@router.get("/tax-rules/{tax_id}/brackets", response_model=List[TaxBracketResponse])
def get_tax_brackets_by_tax_id(
    tax_id: int,
    db: Session = Depends(get_db)
):
    """Get all brackets for a tax rule."""
    repo = TaxBracketsRepository(db)
    service = TaxBracketsService(repo)

    return service.get_brackets_by_tax_id(tax_id)


@router.get("/tax-rules/{tax_id}/active-brackets", response_model=List[TaxBracketResponse])
def get_active_tax_brackets(
    tax_id: int,
    db: Session = Depends(get_db)
):
    """Get active brackets for a tax rule."""
    repo = TaxBracketsRepository(db)
    service = TaxBracketsService(repo)

    return service.get_active_brackets(tax_id)


@router.patch("/tax-brackets/{tax_bracket_id}", response_model=TaxBracketResponse)
def update_tax_bracket(
    tax_bracket_id: int,
    payload: TaxBracketUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(admin_access)
):
    """Update a tax bracket."""
    repo = TaxBracketsRepository(db)
    service = TaxBracketsService(repo)

    tax_bracket = service.update_bracket(
        tax_bracket_id=tax_bracket_id,
        min_amount=payload.min_amount,
        max_amount=payload.max_amount,
        rate=payload.rate,
        description=payload.description,
        deductible_amount=payload.deductible_amount,
        effective_to=payload.effective_to
    )

    if not tax_bracket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tax bracket not found"
        )

    return tax_bracket


@router.delete("/tax-brackets/{tax_bracket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tax_bracket(
    tax_bracket_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(admin_access)
):
    """Delete a tax bracket."""
    repo = TaxBracketsRepository(db)
    service = TaxBracketsService(repo)

    success = service.delete_bracket(tax_bracket_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tax bracket not found"
        )
