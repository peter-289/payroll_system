"""Compatibility shim for misspelled insurance service import.

Some tests and older code import `app.services.insuarance_service` (note
the misspelling). Provide a thin shim that re-exports the real
`InsuranceService` and symbols from `insurance_service`.
"""
from .insurance_service import *  # noqa: F401,F403

__all__ = [name for name in dir() if not name.startswith("_")]
