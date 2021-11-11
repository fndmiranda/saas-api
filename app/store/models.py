import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.address.models import HasAddresses
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
    stores = relationship("Store", back_populates="segment")


class Store(
    Base,
    ModelMixin,
    TimestampMixin,
    HasAddresses,
):
    __tablename__ = "store_stores"

    title = sa.Column(sa.String, nullable=False)
    legal = sa.Column(sa.String, nullable=True)
    external_data = sa.Column(sa.JSON, nullable=True)
    phones = sa.Column(sa.JSON, nullable=True)
    information = sa.Column(sa.JSON, nullable=True)
    automatic_accept = sa.Column(sa.Boolean, nullable=False, default=False)
    is_active = sa.Column(sa.Boolean, nullable=False, default=True)
    document_type = sa.Column(sa.String, nullable=False)
    document_number = sa.Column(sa.String, nullable=False, unique=True)
    approved_at = sa.Column(sa.DateTime, nullable=True)
    image = sa.Column(sa.String, nullable=True)
    background_image = sa.Column(sa.String, nullable=True)
    segment = relationship("Segment", back_populates="stores")
    segment_id = sa.Column(sa.Integer, sa.ForeignKey("store_segments.id"))
    people = relationship(
        "StorePerson",
        back_populates="store",
        lazy="dynamic",
        cascade="all, delete",
    )


class StorePerson(
    Base,
    ModelMixin,
    TimestampMixin,
):
    __tablename__ = "store_people"

    store_id = sa.Column(
        sa.Integer, sa.ForeignKey("store_stores.id"), nullable=False
    )
    user_id = sa.Column(
        sa.Integer, sa.ForeignKey("user_users.id"), nullable=False
    )
    is_owner = sa.Column(sa.Boolean(), nullable=False, default=False)
    is_staff = sa.Column(sa.Boolean(), nullable=False, default=False)
    is_active = sa.Column(sa.Boolean(), nullable=False, default=True)
    store = relationship("Store", back_populates="people")
    user = relationship("User", back_populates="stores")
