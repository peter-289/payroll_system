from typing import List, Callable, Optional
from app.schemas.payroll_schema import PayrollInput, PayrollResult, TaxBreakdownItem, LineItem
from app.exceptions.exceptions import InvalidPayrollInputError, TaxCalculationError


class PayrollEngine:
    """A small, standalone payroll engine designed to be testable and extensible.

    Usage:
        engine = PayrollEngine()
        result = engine.compute(payroll_input)
    """

    def __init__(self, config: Optional[dict] = None) -> None:
        self.config = config or {}
        # simple default progressive brackets if none provided
        self.brackets = self.config.get("tax_brackets", [
            {"lower": 0, "upper": 10000, "rate": 0.0},
            {"lower": 10000, "upper": 30000, "rate": 0.1},
            {"lower": 30000, "upper": 100000, "rate": 0.2},
            {"lower": 100000, "upper": None, "rate": 0.3},
        ])
        # plugin rules: functions that accept context dict and mutate it
        self.pre_tax_rules: List[Callable] = []
        self.post_tax_rules: List[Callable] = []

    def register_pre_tax_rule(self, fn: Callable) -> None:
        self.pre_tax_rules.append(fn)

    def register_post_tax_rule(self, fn: Callable) -> None:
        self.post_tax_rules.append(fn)

    def _validate(self, payload: PayrollInput) -> None:
        if not payload.earnings:
            raise InvalidPayrollInputError("No earnings provided", payload=payload)

    def _sum_items(self, items) -> float:
        return sum((getattr(i, "amount", 0) for i in items), 0.0)

    def _calc_progressive_tax(self, taxable: float) -> tuple[float, List[TaxBreakdownItem]]:
        try:
            remaining = taxable
            total_tax = 0.0
            breakdown: List[TaxBreakdownItem] = []
            for bracket in self.brackets:
                lower = bracket["lower"]
                upper = bracket.get("upper")
                rate = bracket["rate"]
                if taxable <= lower:
                    continue
                upper_bound = upper if upper is not None else taxable
                taxable_in_bracket = max(0.0, min(taxable, upper_bound) - lower)
                if taxable_in_bracket <= 0:
                    continue
                tax_amount = taxable_in_bracket * rate
                total_tax += tax_amount
                breakdown.append(TaxBreakdownItem(name=f"{lower}-{upper}", amount=round(tax_amount, 2), rate=rate))
                remaining -= taxable_in_bracket
                if remaining <= 0:
                    break
            return round(total_tax, 2), breakdown
        except Exception as e:
            raise TaxCalculationError(str(e))

    def compute(self, payload: PayrollInput) -> PayrollResult:
        self._validate(payload)

        # run pre-tax rules to mutate payload/context if needed
        context = {"payload": payload, "meta": {}}
        for rule in self.pre_tax_rules:
            rule(context)

        gross = sum((e.amount for e in payload.earnings))
        taxable_income = sum((e.amount for e in payload.earnings if e.taxable))

        pre_tax_deductions = 0.0
        if payload.deductions:
            pre_tax_deductions = self._sum_items(payload.deductions)

        taxable_after_deductions = max(0.0, taxable_income - pre_tax_deductions)

        tax_total, tax_breakdown = self._calc_progressive_tax(taxable_after_deductions)

        deductions_total = self._sum_items(payload.deductions) if payload.deductions else 0.0
        allowances_total = self._sum_items(payload.allowances) if payload.allowances else 0.0

        net = gross - tax_total - deductions_total + allowances_total

        # post-tax rules
        post_context = {"gross": gross, "tax": tax_total, "net": net, "payload": payload}
        for rule in self.post_tax_rules:
            rule(post_context)

        line_items: List[LineItem] = []
        for e in payload.earnings:
            line_items.append(LineItem(code=e.code, description="earning", amount=e.amount))
        if payload.deductions:
            for d in payload.deductions:
                line_items.append(LineItem(code=d.code, description="deduction", amount=-d.amount))
        if payload.allowances:
            for a in payload.allowances:
                line_items.append(LineItem(code=a.code, description="allowance", amount=a.amount))

        result = PayrollResult(
            employee_id=payload.employee_id,
            period_start=payload.period_start,
            period_end=payload.period_end,
            gross_pay=round(gross, 2),
            taxable_income=round(taxable_after_deductions, 2),
            tax_total=round(tax_total, 2),
            tax_breakdown=tax_breakdown,
            deductions_total=round(deductions_total, 2),
            allowances_total=round(allowances_total, 2),
            net_pay=round(post_context.get("net", net), 2),
            employer_costs=round(self.config.get("employer_multiplier", 0.0) * gross, 2) if self.config.get("employer_multiplier") else 0.0,
            line_items=line_items,
            audit={"engine_version": "1.0", "rules_applied": {"pre_tax": len(self.pre_tax_rules), "post_tax": len(self.post_tax_rules)}},
        )

        return result