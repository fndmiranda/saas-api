import sqlalchemy as sa

from app.core.models import ModelMixin, TimestampMixin
from app.database import Base


class Segment(
    Base,
    ModelMixin,
    TimestampMixin,
):
    __tablename__ = "store_segments"

    title = sa.Column(sa.String, nullable=False)
    is_active = sa.Column(sa.Boolean, nullable=False, default=True)
    image = sa.Column(sa.String, nullable=True)
    color = sa.Column(sa.String, nullable=True)
    # stores = relationship("Store", back_populates="segment")
