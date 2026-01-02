"""Compatibility shim: correct spelling for insurance service (re-exports `insuarance_service`)."""
import warnings
from app.services.insuarance_service import *

warnings.warn(
    "app.services.insurance_service is a compatibility shim for insuarance_service and may be removed in future",
    DeprecationWarning,
)

__all__ = [name for name in globals() if not name.startswith("_")]
