from app.domain.exceptions.base import ValidationError, ValidationError
from decimal import Decimal, InvalidOperation
from app.domain.enums import AllowanceCalculationType, AllowancePercentageBasis


def validate_allowance_amount(
        amount: str | float | Decimal, 
        min_amount: str | float |Decimal,
        max_amount: str | float |Decimal) -> Decimal:
    """Validates allowance amount and enforces min/max limits."""
    try:
        amount = Decimal(amount)
    except (InvalidOperation, TypeError):
        raise ValidationError("Amount must be a valid decimal number.")

    if amount < 0:
        raise ValidationError("Amount cannot be negative.")

    if min_amount is not None and amount < min_amount:
        raise ValidationError(f"Amount must be >= minimum {min_amount}.")

    if max_amount is not None and amount > max_amount:
        raise ValidationError(f"Amount must be <= maximum {max_amount}.")

    return amount


def validate_calculation_basis(
    calculation_type: str | None,
    percentage_base: str | None,
) -> None:
    """Validate rules for percentage-based allowance calculation."""

    if calculation_type == AllowanceCalculationType.PERCENTAGE:
        if not percentage_base:
            raise ValidationError(
                "percentage_base is required for percentage-based allowances."
            )

        if percentage_base not in AllowancePercentageBasis:
            raise ValidationError(
                f"Invalid percentage_base: {percentage_base}"
            )

    else:
        if percentage_base is not None:
            raise ValidationError(
                "percentage_base is only allowed for percentage-based allowances."
            )



def ensure_no_duplicate_allowance(existing_allowance) -> None:
    """Ensures no duplicate allowance exists for the same payroll and type."""
    if existing_allowance:
        raise ValidationError(f"Allowance of type ID {existing_allowance.allowance_type_id} already exists for payroll ID {existing_allowance.payroll_id}.")


def ensure_unique_name(existing_name: str, name: str)-> None:
    """
    Docstring for ensure_unique_name
    
    :param existing_name: Description
    :type existing_name: str
    :param name: Description
    :type name: str
    """
    
    if name == existing_name:
        raise ValidationError("Allowance type with this name already exists.")

