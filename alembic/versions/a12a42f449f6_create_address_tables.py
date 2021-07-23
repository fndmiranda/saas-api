"""Create address tables

Revision ID: a12a42f449f6
Revises: 39203191ad31
Create Date: 2021-07-22 16:09:24.260995

"""
from datetime import datetime

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "a12a42f449f6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "address_addresses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=True),
        sa.Column("is_default", sa.Boolean(), nullable=False),
        sa.Column("street", sa.String(length=255), nullable=False),
        sa.Column("neighborhood", sa.String(length=150), nullable=False),
        sa.Column("city", sa.String(length=150), nullable=False),
        sa.Column("postcode", sa.String(length=9), nullable=False),
        sa.Column("state", sa.String(length=2), nullable=False),
        sa.Column("number", sa.Integer(), nullable=True),
        sa.Column("complement", sa.String(length=150), nullable=True),
        sa.Column("lat", sa.Numeric(11, 4), nullable=True),
        sa.Column("lng", sa.Numeric(11, 4), nullable=True),
        sa.Column("created_at", sa.DateTime, default=datetime.now),
        sa.Column(
            "updated_at",
            sa.DateTime,
            default=datetime.now,
            onupdate=datetime.now,
        ),
        sa.Column("discriminator", sa.String(), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("address_addresses")
