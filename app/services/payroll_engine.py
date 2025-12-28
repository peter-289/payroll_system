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


class PayrollEngine:
    @staticmethod
    def calculate(input: GrossPayInput) -> Decimal:
        if input.base_pay < 0:
            raise ComputeError("Base pay cannot be negative")

        gross = input.base_pay + input.allowance_total

        if input.overtime_hours > 0:
            overtime_pay = (
                input.overtime_rate
                * input.overtime_multiplier
                * input.overtime_hours
            )
            gross += overtime_pay

        return gross.quantize(Decimal("0.00"))
