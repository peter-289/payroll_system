from decimal import Decimal
from app.engines.gross_pay_engine import GrossPayEngine


def test_monthly_full_period_no_overtime():
    base = Decimal("2200.00")
    gross = GrossPayEngine.calculate(base, "monthly")
    assert gross == Decimal("2200.00")


def test_monthly_prorated_and_overtime():
    base = Decimal("2200.00")
    # 11 working days out of 22 -> half pay; 2 hours overtime
    gross = GrossPayEngine.calculate(base, "monthly", worked_days=11, overtime_hours=Decimal("2"))
    # Hourly = 2200 / (22*8) = 12.5; overtime pay = 2 * 12.5 * 1.5 = 37.5
    assert gross == Decimal("1100.00") + Decimal("37.50")


def test_hourly_with_worked_days_and_overtime():
    hourly = Decimal("10.00")
    # worked 10 days -> 80 hours
    gross = GrossPayEngine.calculate(hourly, "hourly", worked_days=10, overtime_hours=Decimal("5"))
    # base = 80 * 10 = 800; overtime = 5 * 10 * 1.5 = 75 => 875
    assert gross == Decimal("875.00")


def test_invalid_frequency():
    try:
        GrossPayEngine.calculate(Decimal("1000"), "weekly")
        assert False, "Expected InvalidPayFrequencyError"
    except Exception as e:
        from app.exceptions.exceptions import InvalidPayFrequencyError

        assert isinstance(e, InvalidPayFrequencyError)
