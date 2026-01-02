"""Compatibility shim: preferred name is `employee_service` (re-exports `user_service`)."""
import warnings
from app.services.user_service import *

warnings.warn(
    "app.services.employee_service is a compatibility shim for user_service and may be removed in future",
    DeprecationWarning,
)

# Re-export public names
__all__ = [name for name in globals() if not name.startswith("_")]
