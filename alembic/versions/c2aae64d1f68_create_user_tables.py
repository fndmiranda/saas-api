"""Create user tables

Revision ID: c2aae64d1f68
Revises:
Create Date: 2021-06-11 13:16:45.431020

"""
from datetime import datetime

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "c2aae64d1f68"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("nickname", sa.String(), nullable=False),
        sa.Column("document_number", sa.String(), nullable=False),
        sa.Column("phones", sa.JSON(), nullable=True),
        sa.Column("avatar", sa.JSON(), nullable=True),
        sa.Column("external_data", sa.JSON(), nullable=True),
        sa.Column("birthdate", sa.Date(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False),
        sa.Column("is_celebrity", sa.Boolean(), nullable=False),
        sa.Column("accept_legal_term", sa.Boolean(), nullable=False),
        sa.Column("email_verified_at", sa.DateTime(), nullable=True),
        sa.Column("salt", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime, default=datetime.now),
        sa.Column(
            "updated_at",
            sa.DateTime,
            default=datetime.now,
            onupdate=datetime.now,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("document_number"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("nickname"),
    )


def downgrade():
    op.drop_table("user_users")
