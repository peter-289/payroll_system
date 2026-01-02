import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app.services.auth_service import AuthService
from app.exceptions.exceptions import InvalidCredentialsError, UserNotFoundError
from payroll_system.app.core.security import hash_password


class FakeQuery:
    def __init__(self, result):
        self._result = result

    def filter(self, *args, **kwargs):
        return self

    def first(self):
        return self._result


class FakeSession:
    def __init__(self, mapping=None):
        self._mapping = mapping or {}

    def query(self, model):
        # return a FakeQuery with the mapped value for the model or None
        return FakeQuery(self._mapping.get(model))


class FakeUser:
    def __init__(self, id, username, password_hash, role_id, must_change_password=False):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role_id = role_id
        self.must_change_password = must_change_password


class FakeRole:
    def __init__(self, id, role_name):
        self.id = id
        self.role_name = role_name


def test_authenticate_user_success():
    # Arrange
    plain_pw = "s3cret"
    user = FakeUser(1, "alice", hash_password(plain_pw), role_id=10, must_change_password=False)
    role = FakeRole(10, "admin")
    fake_db = FakeSession({
        __import__("app.models.user_model", fromlist=["User"]).User: user,
        __import__("app.models.roles_model", fromlist=["Role"]).Role: role,
    })

    service = AuthService(fake_db)

    # Act
    result = service.authenticate_user("alice", plain_pw)

    # Assert
    assert result["user_id"] == 1
    assert "access_token" in result
    assert result["must_change_password"] is False


def test_authenticate_user_invalid_credentials():
    # Arrange
    user = FakeUser(2, "bob", hash_password("correct_pw"), role_id=11)
    role = FakeRole(11, "hr")
    fake_db = FakeSession({
        __import__("app.models.user_model", fromlist=["User"]).User: user,
        __import__("app.models.roles_model", fromlist=["Role"]).Role: role,
    })

    service = AuthService(fake_db)

    # Act & Assert
    with pytest.raises(InvalidCredentialsError):
        service.authenticate_user("bob", "wrong_pw")


def test_change_password_user_not_found():
    # Arrange: session returns None for User queries
    fake_db = FakeSession({
        __import__("app.models.user_model", fromlist=["User"]).User: None
    })

    service = AuthService(fake_db)

    # Act & Assert
    with pytest.raises(UserNotFoundError):
        service.change_password(9999, "newpass123")
