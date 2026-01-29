from decimal import Decimal
from typing import Optional

from app.domain.exceptions.base import InvalidPayFrequencyError


class GrossPayEngine:
    """Simple gross pay calculator used by tests.

    - monthly: base is monthly salary; proration assumes 22 working days
      in a month and 8 hours per day for overtime rate calculation.
    - hourly: base is hourly rate; worked_days -> hours = worked_days * 8
    """

    @staticmethod
    def calculate(base: Decimal, frequency: str, worked_days: Optional[int] = None, overtime_hours: Decimal = Decimal("0")) -> Decimal:
        frequency = (frequency or "").lower()

        if frequency == "monthly":
            if worked_days is not None:
                # prorate based on 22 working days
                prorated = (base * Decimal(worked_days)) / Decimal(22)
            else:
                prorated = Decimal(base)

            # hourly rate for overtime is based on full-month hours (22*8)
            hourly_rate = Decimal(base) / (Decimal(22) * Decimal(8))
            overtime_pay = overtime_hours * hourly_rate * Decimal("1.5")
            return (prorated + overtime_pay).quantize(Decimal("0.01"))

        if frequency == "hourly":
            # base is hourly rate; compute hours from worked_days if provided
            hours = Decimal(0)
            if worked_days is not None:
                hours = Decimal(worked_days) * Decimal(8)
            # base pay
            base_pay = Decimal(base) * hours if hours > 0 else Decimal(base)
            overtime_pay = overtime_hours * Decimal(base) * Decimal("1.5")
            return (base_pay + overtime_pay).quantize(Decimal("0.01"))

        raise InvalidPayFrequencyError(f"Unsupported pay frequency: {frequency}")
