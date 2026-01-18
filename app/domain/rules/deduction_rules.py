from typing import List
from app.domain.exceptions.base import DeductionServiceError
from app.schemas.deduction_schema import DeductionCreate


def validate_bracket(brackets) -> None:
    for bracket in brackets:
        if bracket.fixed_amount < 0:
            raise ValueError("Bracket amounts must be non-negative")
        if bracket.min_amount < 0 or bracket.max_amount < 0:
            raise ValueError("Bracket min and max amounts must be non-negative")
        if bracket.min_amount >= bracket.max_amount:
            raise ValueError("Bracket min_amount must be less than max_amount")
        if bracket.rate is None and bracket.fixed_amount is None:
            raise DeductionServiceError("Bracket must define rate or fixed_amount")
        if bracket.rate is not None and bracket.fixed_amount is not None:
            raise DeductionServiceError("Bracket cannot define both rate and fixed_amount")


def check_unique_names(payload_name:str, existing_name: str) -> None:
    if payload_name == existing_name:
        raise DeductionServiceError("Deduction names must be unique")


