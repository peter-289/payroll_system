"""
Payroll computation engine.

Handles precise calculations for allowances, deductions, gross pay, net pay.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict, Any
from app.schemas.payroll_schema import (
    ResolvedPayrollInputs,
    PayrollResult,
    TaxBreakdownItem,
    LineItem,
    ResolvedAllowance,
    ResolvedDeductionRule,
    PayrollInput,
    EarningItem,
    DeductionItem,
    AllowanceItem,
)
from app.domain.exceptions.base import PayrollComputeError


class PayrollEngine:
    """
    Engine for computing payroll.

    Supports single employee and batch computations.
    """

    def __init__(self, config: dict | None = None):
        self.config = config or {}

    def compute(self, inputs):
        # If a simple PayrollInput is provided (legacy), delegate to compute_simple
        if hasattr(inputs, "earnings"):
            return self.compute_simple(inputs)

        try:
            # Calculate allowances total
            allowances_total = sum(
                allowance.amount for allowance in inputs.allowances
            )

            # Base gross = base_salary + allowances
            gross_pay = inputs.base_salary + allowances_total

            # Add overtime if any
            if inputs.attendance.overtime_hours > 0:
                # Assume overtime rate is base_salary / 160 (assuming 160 hours/month)
                overtime_rate = inputs.base_salary / Decimal('160')
                overtime_pay = inputs.attendance.overtime_hours * overtime_rate * Decimal('1.5')
                gross_pay += overtime_pay

            # Calculate taxable income
            taxable_allowances = sum(
                allowance.amount for allowance in inputs.allowances if allowance.is_taxable
            )
            taxable_income = inputs.base_salary + taxable_allowances

            # Calculate deductions
            deductions_total = Decimal('0')
            tax_breakdown = []
            line_items = []

            # Statutory deductions
            for rule in inputs.statutory_deduction_rules:
                amount = PayrollEngine._calculate_deduction_amount(rule, taxable_income)
                deductions_total += amount
                line_items.append(LineItem(
                    code=rule.code,
                    description=rule.name,
                    amount=float(amount)
                ))
                if rule.code.upper() == 'PAYE':
                    tax_breakdown.append(TaxBreakdownItem(
                        name=rule.name,
                        amount=float(amount),
                        rate=float(rule.rate or 0)
                    ))

            # Loan deduction
            if inputs.loan.monthly_repayment > 0:
                deductions_total += inputs.loan.monthly_repayment
                line_items.append(LineItem(
                    code='LOAN',
                    description='Loan Repayment',
                    amount=float(inputs.loan.monthly_repayment)
                ))

            # Insurance
            if inputs.insurance.employee_contribution > 0:
                deductions_total += inputs.insurance.employee_contribution
                line_items.append(LineItem(
                    code='INSURANCE',
                    description='Insurance Contribution',
                    amount=float(inputs.insurance.employee_contribution)
                ))

            # Pension
            if inputs.pension.employee_contribution > 0:
                deductions_total += inputs.pension.employee_contribution
                line_items.append(LineItem(
                    code='PENSION',
                    description='Pension Contribution',
                    amount=float(inputs.pension.employee_contribution)
                ))

            # Net pay
            net_pay = gross_pay - deductions_total

            # Tax total (assuming PAYE is the tax)
            tax_total = sum(item.amount for item in tax_breakdown)

            # Employer costs (for now, just gross + employer contributions)
            employer_costs = gross_pay  # TODO: add employer pension/insurance if needed

            return PayrollResult(
                employee_id=inputs.employee_id,
                period_start=inputs.period_start,
                period_end=inputs.period_end,
                gross_pay=float(gross_pay),
                taxable_income=float(taxable_income),
                tax_total=tax_total,
                tax_breakdown=tax_breakdown,
                deductions_total=float(deductions_total),
                allowances_total=float(allowances_total),
                net_pay=float(net_pay),
                employer_costs=float(employer_costs),
                line_items=line_items,
                audit={"computed_at": "now"}  # TODO: add timestamp
            )

        except Exception as e:
            raise PayrollComputeError(f"Failed to compute payroll: {str(e)}")

    def compute_simple(self, payload: PayrollInput) -> PayrollResult:
        """
        Compute payroll for simple PayrollInput (backwards compatibility).
        Uses `self.config.get('tax_brackets')` when provided, otherwise no tax.
        """
        try:
            # Gross pay from all earnings (taxable and non-taxable)
            gross_pay = sum(item.amount for item in payload.earnings)

            # Allowances total
            allowances_total = sum(item.amount for item in payload.allowances or [])

            # Deductions total
            deductions_total = sum(item.amount for item in payload.deductions or [])

            # Taxable income = taxable earnings - pre-tax deductions
            taxable_earnings = sum(item.amount for item in payload.earnings if getattr(item, 'taxable', False))
            taxable_income = taxable_earnings - deductions_total
            if taxable_income < 0:
                taxable_income = 0

            # Tax calculation
            tax_total = 0.0
            tax_breakdown = []
            brackets = self.config.get('tax_brackets') if hasattr(self, 'config') else None
            if brackets:
                remaining = taxable_income
                for b in brackets:
                    lower = b.get('lower', 0)
                    upper = b.get('upper')
                    rate = b.get('rate', 0)
                    if upper is None:
                        taxable_in_band = max(0, remaining)
                    else:
                        taxable_in_band = max(0, min(remaining, upper - lower))
                    band_tax = taxable_in_band * rate
                    if taxable_in_band > 0:
                        tax_breakdown.append(TaxBreakdownItem(name=f"{int(rate*100)}% band", amount=band_tax, rate=rate*100))
                    tax_total += band_tax
                    remaining -= taxable_in_band
                    if remaining <= 0:
                        break
            else:
                # default: no tax
                tax_total = 0.0
                tax_breakdown = [TaxBreakdownItem(name="Income Tax", amount=tax_total, rate=0.0)]

            # Net pay
            net_pay = gross_pay - deductions_total - tax_total + allowances_total

            # Line items
            line_items = [
                LineItem(code=item.code, description=f"Earning: {item.code}", amount=item.amount)
                for item in payload.earnings
            ] + [
                LineItem(code=item.code, description=f"Allowance: {item.code}", amount=item.amount)
                for item in (payload.allowances or [])
            ] + [
                LineItem(code=item.code, description=f"Deduction: {item.code}", amount=item.amount)
                for item in (payload.deductions or [])
            ]

            return PayrollResult(
                employee_id=payload.employee_id,
                period_start=payload.period_start,
                period_end=payload.period_end,
                gross_pay=gross_pay,
                taxable_income=taxable_income,
                tax_total=tax_total,
                tax_breakdown=tax_breakdown,
                deductions_total=deductions_total,
                allowances_total=allowances_total,
                net_pay=net_pay,
                employer_costs=gross_pay,
                line_items=line_items,
                audit={"engine_version": self.config.get("engine_version", "1.0")}
            )

        except Exception as e:
            raise PayrollComputeError(f"Failed to compute payroll: {str(e)}")

    @staticmethod
    def _calculate_deduction_amount(rule: ResolvedDeductionRule, taxable_income: Decimal) -> Decimal:
        """
        Calculate deduction amount based on rule.
        """
        if rule.has_brackets and rule.brackets:
            # Tiered calculation
            amount = Decimal('0')
            remaining = taxable_income
            for bracket in rule.brackets:
                if remaining <= 0:
                    break
                bracket_min = bracket.get('min_amount', Decimal('0'))
                bracket_max = bracket.get('max_amount')
                rate = bracket.get('rate', Decimal('0'))
                if bracket_max is None or remaining < bracket_max:
                    taxable_in_bracket = remaining - bracket_min
                else:
                    taxable_in_bracket = bracket_max - bracket_min
                amount += taxable_in_bracket * (rate / Decimal('100'))
                remaining -= taxable_in_bracket
            return amount
        elif rule.rate:
            return taxable_income * (rule.rate / Decimal('100'))
        elif rule.fixed_amount:
            return rule.fixed_amount
        else:
            return Decimal('0')