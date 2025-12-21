import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.payroll_engine import PayrollEngine
from app.schemas.payroll_schema import PayrollInput, EarningItem, DeductionItem, AllowanceItem
from datetime import date


def test_simple_payroll_no_deductions():
    """Test basic payroll with only earnings."""
    engine = PayrollEngine()
    payload = PayrollInput(
        employee_id=1,
        period_start=date(2025, 12, 1),
        period_end=date(2025, 12, 31),
        earnings=[EarningItem(code="basic", amount=2000.0, taxable=True)],
        deductions=[],
        allowances=[],
    )
    result = engine.compute(payload)
    assert result.employee_id == 1
    assert result.gross_pay == 2000.0
    # Taxable income should be 2000 minus 0 pre-tax deductions
    assert result.taxable_income == 2000.0
    # Tax should be: 0 (0-10k rate 0%) = 0
    assert result.tax_total == 0.0
    # Net = gross - tax - deductions + allowances = 2000 - 0 - 0 + 0
    assert result.net_pay == 2000.0


def test_payroll_with_deductions_and_allowances():
    """Test payroll with deductions, allowances, and custom tax brackets."""
    engine = PayrollEngine(config={"tax_brackets": [{"lower": 0, "upper": 1000, "rate": 0.0}, {"lower": 1000, "upper": None, "rate": 0.1}]})
    payload = PayrollInput(
        employee_id=2,
        period_start=date(2025, 12, 1),
        period_end=date(2025, 12, 31),
        earnings=[
            EarningItem(code="basic", amount=3000.0, taxable=True),
            EarningItem(code="bonus", amount=500.0, taxable=False)
        ],
        deductions=[DeductionItem(code="loan", amount=200.0)],
        allowances=[AllowanceItem(code="transport", amount=50.0)],
    )
    result = engine.compute(payload)
    # Gross includes both taxable and non-taxable earnings
    assert result.gross_pay == 3500.0
    # Taxable income = 3000 (taxable earnings) - 200 (deductions) = 2800
    assert result.taxable_income == 2800.0
    # Tax: 0-1000 at 0% = 0, 1000-2800 at 10% = 180
    assert result.tax_total == 180.0
    # Deductions total
    assert result.deductions_total == 200.0
    # Allowances total
    assert result.allowances_total == 50.0
    # Net = 3500 - 180 (tax) - 200 (deductions) + 50 (allowances) = 3170
    assert result.net_pay == 3170.0
