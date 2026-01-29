from app.domain.exceptions.base import DomainError


def validate_id(id: int) -> None:
    """
    Docstring for validate_id
    
    :param id: Any integer ID
    :type id: int
    """
    if id <= 0:
        raise DomainError("Invalid ID")