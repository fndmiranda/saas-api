import pytest


@pytest.fixture
def account_create():
    return {
        "name": "Fernando",
        "email": "fndmiranda@gmail.com",
        "accept_legal_term": True,
        "nickname": "fndmiranda",
        "document_number": "57726785071",
        "password": "test_password",
        "birthdate": "1983-06-07",
    }


@pytest.fixture
def account_update():
    return {
        "name": "Testing",
        "email": "update@testing.com",
        "accept_legal_term": True,
        "nickname": "testing",
        "document_number": "15614534040",
        "password": "test_password_update",
        "birthdate": "1982-06-01",
    }
