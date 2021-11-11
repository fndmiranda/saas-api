import sqlalchemy as sa
from sqlalchemy import and_, event
from sqlalchemy.orm import backref, foreign, relationship, remote

from app.core.models import ModelMixin
from app.database import Base


class Address(Base, ModelMixin):
    """The Address class.

    This represents all address records in a
    single table.

    """

    __tablename__ = "address_addresses"

    name = sa.Column(sa.String, nullable=True)
    is_default = sa.Column(sa.Boolean, nullable=False, default=False)
    street = sa.Column(sa.String, nullable=False)
    neighborhood = sa.Column(sa.String, nullable=False)
    city = sa.Column(sa.String, nullable=False)
    postcode = sa.Column(sa.String, nullable=False)
    state = sa.Column(sa.String, nullable=False)
    number = sa.Column(sa.Integer, nullable=True)
    complement = sa.Column(sa.String, nullable=True)
    lat = sa.Column(sa.Float, nullable=True)
    lng = sa.Column(sa.Float, nullable=True)

    discriminator = sa.Column(sa.String)
    """Refers to the type of parent."""

    parent_id = sa.Column(sa.Integer)
    """Refers to the primary key of the parent.

    This could refer to any table.
    """

    @property
    def parent(self):
        """Provides in-Python access to the "parent" by choosing
        the appropriate relationship.

        """
        return getattr(self, "parent_%s" % self.discriminator)

    def __repr__(self):
        return "%s(postcode=%r, state=%r, city=%r)" % (
            self.__class__.__name__,
            self.postcode,
            self.state,
            self.city,
        )


class HasAddresses(object):
    """HasAddresses mixin, creates a new address_association
    table for each parent.

    """


@event.listens_for(HasAddresses, "mapper_configured", propagate=True)
def setup_listener(mapper, class_):
    name = class_.__name__
    discriminator = name.lower()
    class_.addresses = relationship(
        Address,
        primaryjoin=and_(
            class_.id == foreign(remote(Address.parent_id)),
            Address.discriminator == discriminator,
        ),
        backref=backref(
            "parent_%s" % discriminator,
            primaryjoin=remote(class_.id) == foreign(Address.parent_id),
        ),
        lazy="subquery",
        cascade="all, delete",
    )

    @event.listens_for(class_.addresses, "append")
    def append_address(target, value, initiator):
        value.discriminator = discriminator
