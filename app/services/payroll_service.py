"""Compatibility module exposing payroll engine and resolution helpers as `payroll_service`."""
import warnings
from app.services.payroll_engine import PayrollEngine, GrossPayInput, ComputeError
from app.services.payroll_resolution_service import PayrollResolutionService

warnings.warn(
    "app.services.payroll_service is a compatibility wrapper; prefer using PayrollEngine or PayrollResolutionService directly",
    DeprecationWarning,
)

__all__ = ["PayrollEngine", "GrossPayInput", "ComputeError", "PayrollResolutionService"]
