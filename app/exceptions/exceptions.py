"""Compatibility exceptions package.

This module re-exports domain exceptions under `app.exceptions.exceptions`
to keep imports in tests and older code working.
"""
from app.domain.exceptions.base import *  # noqa: F401,F403
from app.domain.exceptions.base import DomainError

# Backwards-compatible aliases used by some tests/older modules.
InsuranceServiceError = DomainError
EmployeeServiceError = DomainError

__all__ = [name for name in dir() if not name.startswith("_")]
