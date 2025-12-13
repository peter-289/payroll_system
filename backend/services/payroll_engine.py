from decimal import Decimal
from typing import Dict

class PayrollEngine:
    def __init__(self):
        pass

class GrossCalculator:
    def __init__(self,
        base_salary:Decimal,
        allowances:Dict[str, Decimal],
        position_multiplier: Decimal = Decimal("1.0"),
        department_multiplier: Decimal = Decimal("1.0")
):
        self.base_salary = base_salary
        self.allowances = allowances
        self.position_multiplier = position_multiplier
        self.department_multiplier = department_multiplier

    def compute(self) -> Dict[str, Decimal]:
        adjusted_base = (
            self.base_salary
            * self.position_multiplier
            * self.department_multiplier
        )

        total_allowances = sum(self.allowances.values()) if self.allowances else Decimal("0.00")

        gross_salary = adjusted_base + total_allowances

        return {
            "adjusted_base_salary": adjusted_base,
            "total_allowances": total_allowances,
            "gross_salary": gross_salary,
        }
    

