import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from datetime import datetime
from app.services.insuarance_service import InsuranceService
from app.exceptions.exceptions import InsuranceServiceError, InsuranceRecordNotFoundError


class FakeQuery:
    def __init__(self, result=None):
        self._result = result

    def filter(self, *args, **kwargs):
        return self

    def first(self):
        return self._result


class FakeSession:
    def __init__(self, mapping=None):
        # mapping: model_class -> return_value
        self._mapping = mapping or {}
        self._added = []
        self._committed = False
        self._rolled_back = False

    def query(self, model):
        return FakeQuery(self._mapping.get(model))

    def add(self, obj):
        self._added.append(obj)

    def commit(self):
        self._committed = True

    def rollback(self):
        self._rolled_back = True

    def refresh(self, obj):
        # simulate DB assigning id
        if not getattr(obj, 'id', None):
            obj.id = 123

    def get(self, model, id):
        return self._mapping.get(('get', model, id), None)

    def delete(self, obj):
        # simulate delete by marking a flag
        obj._deleted = True


class FakeInsurance:
    def __init__(self, id=None, policy_number=None, status='active'):
        self.id = id
        self.policy_number = policy_number
        self.status = status
        self.end_date = None


def test_create_insurance_duplicate_policy_raises():
    # Arrange: query returns existing policy
    Insurance = __import__('app.models.Insuarance_model', fromlist=['Insurance']).Insurance
    fake_existing = FakeInsurance(id=1, policy_number='POL-EXIST')
    fake_db = FakeSession({Insurance: fake_existing})
    service = InsuranceService(fake_db)

    # Monkeypatch _generate_policy_number to return existing policy number
    service._generate_policy_number = lambda: 'POL-EXIST'

    # Act & Assert
    with pytest.raises(InsuranceServiceError):
        service.create_insurance(
            type('P', (), {
                'employee_id': 1,
                'insurance_provider': 'Prov',
                'coverage_type': 'Full',
                'premium_amount': 100.0,
                'employer_contribution': 50.0,
                'employee_contribution': 50.0,
                'start_date': datetime.utcnow(),
                'end_date': None,
                'status': 'active'
            })
        )


def test_get_policy_not_found_raises():
    Insurance = __import__('app.models.Insuarance_model', fromlist=['Insurance']).Insurance
    fake_db = FakeSession({Insurance: None})
    service = InsuranceService(fake_db)

    with pytest.raises(InsuranceRecordNotFoundError):
        service.get_policy(9999)


def test_soft_delete_policy_success():
    Insurance = __import__('app.models.Insuarance_model', fromlist=['Insurance']).Insurance
    fake_policy = FakeInsurance(id=5, policy_number='POL-123', status='active')
    fake_db = FakeSession({('get', Insurance, 5): fake_policy})
    service = InsuranceService(fake_db)

    result = service.soft_delete_policy(5)

    assert result['message'] == 'Policy cancelled successfully'
    assert fake_policy.status == 'cancelled'
    assert fake_db._committed is True


def test_delete_policy_not_found_raises():
    Insurance = __import__('app.models.Insuarance_model', fromlist=['Insurance']).Insurance
    fake_db = FakeSession({Insurance: None})
    service = InsuranceService(fake_db)

    with pytest.raises(InsuranceRecordNotFoundError):
        service.delete_policy(7777)
