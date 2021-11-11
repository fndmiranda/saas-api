import pytest


@pytest.fixture
def account_primary():
    return {
        "name": "Fernando",
        "email": "fndmiranda@gmail.com",
        "accept_legal_term": True,
        "nickname": "fndmiranda",
        "document_number": "57726785071",
        "password": "test_password_primary",
        "birthdate": "1983-06-07",
    }


@pytest.fixture
def account_secondary():
    return {
        "name": "Testing secondary",
        "email": "secondary@testing.com",
        "accept_legal_term": True,
        "nickname": "secondary",
        "document_number": "22802262009",
        "password": "test_password_secondary",
        "birthdate": "2000-08-03",
    }
