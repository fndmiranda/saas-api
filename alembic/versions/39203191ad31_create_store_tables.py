"""Create store tables

Revision ID: 39203191ad31
Revises: c2aae64d1f68
Create Date: 2021-06-19 00:20:04.231222

"""
from datetime import datetime

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "39203191ad31"
down_revision = "c2aae64d1f68"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "store_segments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("color", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("image", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime, default=datetime.now),
        sa.Column(
            "updated_at",
            sa.DateTime,
            default=datetime.now,
            onupdate=datetime.now,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "store_stores",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("legal", sa.String(), nullable=True),
        sa.Column("external_data", sa.JSON(), nullable=True),
        sa.Column("phones", sa.JSON(), nullable=True),
        sa.Column("information", sa.JSON(), nullable=True),
        sa.Column("automatic_accept", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("document_type", sa.String(), nullable=False),
        sa.Column("document_number", sa.String(), nullable=False),
        sa.Column("approved_at", sa.DateTime(), nullable=True),
        sa.Column("segment_id", sa.Integer(), nullable=True),
        sa.Column("image", sa.String(), nullable=True),
        sa.Column("background_image", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime, default=datetime.now),
        sa.Column(
            "updated_at",
            sa.DateTime,
            default=datetime.now,
            onupdate=datetime.now,
        ),
        sa.ForeignKeyConstraint(
            ["segment_id"],
            ["store_segments.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("document_number"),
    )
    op.create_table(
        "store_people",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("store_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("is_owner", sa.Boolean(), nullable=False),
        sa.Column("is_staff", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime, default=datetime.now),
        sa.Column(
            "updated_at",
            sa.DateTime,
            default=datetime.now,
            onupdate=datetime.now,
        ),
        sa.ForeignKeyConstraint(
            ["store_id"],
            ["store_stores.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user_users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("store_people")
    op.drop_table("store_stores")
    op.drop_table("store_segments")
