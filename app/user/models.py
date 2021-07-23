import crypt
from hmac import compare_digest as compare_hash

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.address.models import HasAddresses
from app.core.models import ModelMixin, TimestampMixin
from app.database import Base


class User(
    Base,
    ModelMixin,
    TimestampMixin,
    HasAddresses,
):
    __tablename__ = "user_users"

    name = sa.Column(sa.String(255), nullable=False)
    email = sa.Column(sa.String(255), nullable=False, unique=True)
    nickname = sa.Column(sa.String(128), nullable=False, unique=True)
    document_number = sa.Column(sa.String(32), nullable=False, unique=True)
    external_data = sa.Column(sa.JSON(), nullable=True)
    phones = sa.Column(sa.JSON(), nullable=True)
    avatar = sa.Column(sa.JSON(), nullable=True)
    birthdate = sa.Column(sa.Date(), nullable=False)
    _password = sa.Column("password", sa.String(255), nullable=False)
    is_admin = sa.Column(sa.Boolean(), nullable=False, default=False)
    is_celebrity = sa.Column(sa.Boolean(), nullable=False, default=False)
    accept_legal_term = sa.Column(sa.Boolean(), nullable=False, default=False)
    email_verified_at = sa.Column(sa.DateTime, nullable=True)
    salt = sa.Column(sa.String(128), nullable=False)
    stores = relationship(
        "StorePerson", back_populates="user", cascade="all, delete"
    )

    # define password getter
    @property
    def password(self):
        return self._password

    # define password setter
    @password.setter
    def password(self, value):
        self.salt = crypt.mksalt(crypt.METHOD_SHA256)
        self._password = crypt.crypt(value, self.salt)

    def check_password(self, password):
        return compare_hash(crypt.crypt(password, self.salt), self.password)
