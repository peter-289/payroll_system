import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.payroll_engine import PayrollEngine
from app.schemas.payroll_schema import PayrollInput, EarningItem, DeductionItem, AllowanceItem, PayrollResult
from datetime import date


def test_integration_compute_employee_payroll():
    """Test full payroll computation end-to-end via service."""
    engine = PayrollEngine()
    
    payload = PayrollInput(
        employee_id=1,
        period_start=date(2025, 12, 1),
        period_end=date(2025, 12, 31),
        earnings=[EarningItem(code="salary", amount=5000.0, taxable=True)],
        deductions=[DeductionItem(code="pension", amount=500.0)],
        allowances=[AllowanceItem(code="transport", amount=200.0)],
    )
    
    result = engine.compute(payload)
    
    # Assertions
    assert isinstance(result, PayrollResult)
    assert result.employee_id == 1
    assert result.gross_pay == 5000.0
    assert result.deductions_total == 500.0
    assert result.allowances_total == 200.0
    # Taxable = 5000 - 500 = 4500
    # Default brackets: 0-10k at 0%, so tax = 0
    assert result.tax_total == 0.0
    # Net = 5000 - 0 (tax) - 500 (deductions) + 200 (allowances) = 4700
    assert result.net_pay == 4700.0
    assert "engine_version" in result.audit
    print(f"Payroll result: {result.model_dump()}")


def test_progressive_tax_calculation():
    """Test progressive tax brackets logic."""
    # Custom brackets: 0-2000 @5%, 2000-5000 @15%, 5000+ @25%
    engine = PayrollEngine(config={
        "tax_brackets": [
            {"lower": 0, "upper": 2000, "rate": 0.05},
            {"lower": 2000, "upper": 5000, "rate": 0.15},
            {"lower": 5000, "upper": None, "rate": 0.25},
        ]
    })
    
    payload = PayrollInput(
        employee_id=2,
        period_start=date(2025, 12, 1),
        period_end=date(2025, 12, 31),
        earnings=[EarningItem(code="salary", amount=6000.0, taxable=True)],
    )
    
    result = engine.compute(payload)
    
    # Tax: 2000*0.05 + 3000*0.15 + 1000*0.25 = 100 + 450 + 250 = 800
    assert result.tax_total == 800.0
    assert result.net_pay == 5200.0
    assert len(result.tax_breakdown) > 0
    print(f"Tax breakdown: {result.tax_breakdown}")
