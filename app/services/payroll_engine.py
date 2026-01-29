# Compatibility wrapper: re-export the full PayrollEngine implementation
# from the `app.payroll` package so tests importing
# `app.services.payroll_engine.PayrollEngine` get the correct class.
from decimal import Decimal
from dataclasses import dataclass

class ComputeError(Exception):
    pass


@dataclass(frozen=True)
class GrossPayInput:
    base_pay: Decimal
    allowance_total: Decimal
    overtime_hours: Decimal
    overtime_rate: Decimal  # already resolved
    overtime_multiplier: Decimal = Decimal("1.5")

from app.payroll.payroll_engine import PayrollEngine  # noqa: F401
