from decimal import Decimal, InvalidOperation
from typing import List, Dict, Any, Sequence, Tuple

def _to_decimal(value: Any) -> Decimal | None:
    """Convert a value to Decimal, return None if conversion fails."""
    if value is None or value == '' or str(value).strip() == '':
        return None
    s = str(value).strip().replace(",","").replace(" ","")
    if s.lower() in {"n/a", "none", "null", "none"}:
        return None
    try:
        result = Decimal(s)
        #print(f"Converted value: {s} to Decimal: {result}")
        return result
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError(f"Invalid decimal value: {value}")

# ===================================================================================================
def validate_no_overlaps(brackes:Sequence[Any]) -> Tuple[bool, str | None]:
    if not brackes:
        return True, None
    def get_min(b) -> Decimal:
        try:
            if isinstance(b,dict):
                val = b.get("min_amount") or b.get("min")
            elif isinstance(b, (list, tuple)):
                val = b[0]
            else:  
                val = getattr(b, "min_amount", None) or getattr(b, "min", None)
            result = _to_decimal(val)
            if result is None:
                raise ValueError("min_amount is missing or invalid")
            return result
        except Exception as e:
            raise ValueError(f"Invalid min_amount in bracket {b}: {e}")
        
    def get_max(b) -> Decimal | None:
        try:
            if isinstance(b, dict):
                val = b.get("max_amount") or b.get("max")
            elif isinstance(b, (list, tuple)):
                val = b[1] if len(b) > 1 else None
            else:
                val = getattr(b, "max_amount", None) or getattr(b, "max", None)
            return _to_decimal(val)   # None is allowed for open-ended top bracket
        except Exception:
            return None
    try:
        sorted_brackets = sorted(brackes, key=get_min)
    except ValueError as e:
        return False, str(e)
    previous_max: Decimal | None = None

    for i, bracket in enumerate(sorted_brackets):
        current_min = get_min(bracket)
        current_max = get_max(bracket)

        if previous_max is not None:
            if previous_max is None:
                return False, f"Bracket {i} has no upper limit, cannot have subsequent brackets."
            if current_min < previous_max:
                return False, f"Bracket {i} overlaps with previous bracket."

        previous_max = current_max
    return True, None


brackets_example = [
    {"min_amount": "0", "max_amount": "10000"}
]
is_valid, error_msg = validate_no_overlaps(brackets_example)
if is_valid:
    print("Brackets are valid and non-overlapping.")
else:
    print(f"Error: {error_msg}")