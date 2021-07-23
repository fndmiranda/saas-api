import factory.fuzzy

from app.store.models import Segment, Store
from tests.app.core.factories import BaseFactory


class SegmentFactory(BaseFactory):
    """Factory for segment model."""

    class Meta:
        model = Segment

    title = factory.Sequence(lambda n: "The segment title %d" % n)
    is_active = True
    image = factory.Sequence(lambda n: "image_url_%d.jpg" % n)
    color = factory.Faker("hex_color")


class StoreFactory(BaseFactory):
    """Factory for store model."""

    class Meta:
        model = Store

    title = factory.Sequence(lambda n: 'The store title %d' % n)
    legal = factory.Sequence(lambda n: 'The store legal %d' % n)
    phones = [{"default": True, "name": "Principal", "number": "34999925530"}]
    information = {
        "summary": 'The store summary',
        "mon_time": [{"start": "18:00", "end": "22:00"}],
        "tue_time": [
            {"start": "07:00", "end": "11:00"},
            {"start": "12:30", "end": "18:00"},
        ],
        "wed_time": [{"start": "18:00", "end": "22:00"}],
        "thu_time": [{"start": "18:00", "end": "23:00"}],
        "fri_time": [
            {"start": "07:00", "end": "11:00"},
            {"start": "12:30", "end": "18:00"},
        ],
        "sat_time": [{"start": "18:00", "end": "23:00"}],
        "sun_time": [{"start": "18:00", "end": "23:00"}],
    }
    is_active = True
    document_type = "cpf"
    document_number = factory.Sequence(
        lambda n: 'store_document_number_%d' % n)
    approved_at = None
    # segment = factory.SubFactory(SegmentFactory)
    image = factory.Sequence(lambda n: 'image_url_%d.jpg' % n)
    background_image = factory.Sequence(
        lambda n: 'background_image_url_%d.jpg' % n)
