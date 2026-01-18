from datetime import date, timedelta
import pytest

from app.domain.rules.employee_rules import validate_hire_date_not_future, validate_salary_type
from app.models.employee_model import SalaryTypeEnum


def test_validate_hire_date_not_future_raises_for_future_date():
    future = date.today() + timedelta(days=1)
    with pytest.raises(Exception):
        validate_hire_date_not_future(future)


def test_validate_hire_date_ok_for_today_or_past():
    validate_hire_date_not_future(date.today())
    validate_hire_date_not_future(date.today() - timedelta(days=1))


def test_validate_salary_type_accepts_enum_and_str_and_rejects_invalid():
    validate_salary_type(SalaryTypeEnum.MONTHLY)
    validate_salary_type("monthly")
    with pytest.raises(Exception):
        validate_salary_type("yearly")
