import pytest


@pytest.fixture
def account_create_body():
    return {
        "name": "Fernando",
        "email": "fndmiranda@gmail.com",
        "accept_legal_term": True,
        "nickname": "fndmiranda",
        "document_number": "57726785071",
        "password": "testpass",
        "birthdate": "1983-06-07",
    }
