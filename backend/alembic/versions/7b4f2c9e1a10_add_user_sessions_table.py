"""add user sessions table

Revision ID: 7b4f2c9e1a10
Revises: 68a1d9834a82
Create Date: 2026-07-29

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "7b4f2c9e1a10"
down_revision: Union[str, Sequence[str], None] = "68a1d9834a82"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create persistent authenticated user sessions."""

    op.create_table(
        "user_sessions",
        sa.Column(
            "id",
            sa.String(length=36),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.String(length=36),
            nullable=False,
        ),
        sa.Column(
            "refresh_token_hash",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "device_name",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "ip_address",
            sa.String(length=45),
            nullable=True,
        ),
        sa.Column(
            "user_agent",
            sa.String(length=1000),
            nullable=True,
        ),
        sa.Column(
            "expires_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "last_used_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "is_revoked",
            sa.Boolean(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_user_sessions_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f("pk_user_sessions"),
        ),
        sa.UniqueConstraint(
            "refresh_token_hash",
            name=op.f("uq_user_sessions_refresh_token_hash"),
        ),
    )

    op.create_index(
        op.f("ix_user_sessions_user_id"),
        "user_sessions",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    """Remove persistent authenticated user sessions."""

    op.drop_index(
        op.f("ix_user_sessions_user_id"),
        table_name="user_sessions",
    )

    op.drop_table("user_sessions")
