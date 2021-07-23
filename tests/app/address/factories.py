import factory.fuzzy

from app.address.models import Address
from tests.app.core.factories import BaseFactory


class AddressFactory(BaseFactory):
    """Factory for address model."""

    class Meta:
        model = Address

    street = factory.Faker('street_name')
    city = factory.Faker('city')
    postcode = factory.Faker('postcode', formatted=False)
    name = factory.Sequence(lambda n: 'address_name_%d' % n)
    is_default = False
    state = factory.Faker('state_abbr')
    neighborhood = factory.Faker('neighborhood')
    number = factory.Faker('pyint')
    complement = factory.Sequence(lambda n: 'address_complement_%d' % n)
    lat = factory.Faker('pyfloat', left_digits=2, right_digits=4)
    lng = factory.Faker('pyfloat', left_digits=2, right_digits=4)
