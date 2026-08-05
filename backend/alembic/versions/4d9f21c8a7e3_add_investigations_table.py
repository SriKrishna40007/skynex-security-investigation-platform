"""add investigations table

Revision ID: 4d9f21c8a7e3
Revises: 7b4f2c9e1a10
Create Date: 2026-07-31
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "4d9f21c8a7e3"
down_revision: Union[str, Sequence[str], None] = "7b4f2c9e1a10"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create persistent investigation records."""

    op.create_table(
        "investigations",
        sa.Column(
            "id",
            sa.String(length=36),
            nullable=False,
        ),
        sa.Column(
            "owner_id",
            sa.String(length=36),
            nullable=False,
        ),
        sa.Column(
            "investigation_type",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "risk_score",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "severity",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "summary",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "result",
            sa.JSON(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["users.id"],
            name=op.f("fk_investigations_owner_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f("pk_investigations"),
        ),
    )

    op.create_index(
        op.f("ix_investigations_owner_id"),
        "investigations",
        ["owner_id"],
        unique=False,
    )


def downgrade() -> None:
    """Remove persistent investigation records."""

    op.drop_index(
        op.f("ix_investigations_owner_id"),
        table_name="investigations",
    )

    op.drop_table("investigations")
