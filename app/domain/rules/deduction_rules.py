from typing import Optional
from app.domain.exceptions.base import ValidationError


def validate_bracket(brackets) -> None:
    for bracket in brackets:
        #if bracket.fixed_amount < 0:
            #raise ValueError("Bracket amounts must be non-negative")
        if bracket.min_amount < 0 or bracket.max_amount < 0:
            raise ValueError("Bracket min and max amounts must be non-negative")
        if bracket.min_amount >= bracket.max_amount:
            raise ValueError("Bracket min_amount must be less than max_amount")
        if bracket.rate is None and bracket.fixed_amount is None:
            raise ValidationError("Bracket must define rate or fixed_amount")
        if bracket.rate is not None and bracket.fixed_amount is not None:
            raise ValidationError("Bracket cannot define both rate and fixed_amount")


def check_unique_names(payload_name:str, existing_name: str) -> None:
    """
    Docstring for check_unique_names
    
    :param payload_name: Any payload with attributes can be passed
    :type payload_name: str
    :param existing_name: A name that is to be checked against the payload if it exists
    :type existing_name: str
    """
    if payload_name == existing_name:
        raise ValidationError("Deduction names must be unique")


def ensure_no_duplicate_deduction_type(existing, new_name: str) -> None:
    """
    Docstring for ensure_no_duplicate_deduction_type
    
    :param existing: can be any object
    :type existing: Optional
    :param new_name: A name to be checked against existing object's name
    :type new_name: str
    """
    if existing and existing.name == new_name:
        raise ValidationError("Deduction type with this name already exists")