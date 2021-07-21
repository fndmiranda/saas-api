import factory.fuzzy

from app.store.models import Segment
from tests.app.core.factories import BaseFactory


class SegmentFactory(BaseFactory):
    """Factory for store segment model."""

    class Meta:
        model = Segment

    title = factory.Sequence(lambda n: "The segment title %d" % n)
    is_active = True
    image = factory.Sequence(lambda n: "image_url_%d.jpg" % n)
    color = factory.Faker("hex_color")
