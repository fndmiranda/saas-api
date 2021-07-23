from datetime import date, datetime

import factory

from app.user.models import User
from tests.app.core.factories import BaseFactory


class UserFactory(BaseFactory):
    """Factory for user model."""

    name = factory.Sequence(lambda n: "User %d" % n)
    email = factory.Sequence(lambda n: "user.email_%d@example.com" % n)
    nickname = factory.Sequence(lambda n: "nickname_%d" % n)
    document_number = factory.Faker("cpf")
    phones = [{"default": True, "name": "Principal", "number": 34999925530}]
    birthdate = date.today()
    accept_legal_term = True
    is_admin = False
    is_celebrity = False
    password = "testpass"
    email_verified_at = datetime.now()

    class Meta:
        model = User
