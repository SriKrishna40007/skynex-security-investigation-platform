"""add email verification support

Revision ID: 8f3c2a1d9b44
Revises: 4d9f21c8a7e3
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "8f3c2a1d9b44"
down_revision: Union[str, Sequence[str], None] = "4d9f21c8a7e3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add email verification state and verification tokens."""

    op.add_column(
        "users",
        sa.Column(
            "email_verified_at",
            sa.DateTime(),
            nullable=True,
        ),
    )

    op.create_table(
        "email_verification_tokens",
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
            "token_hash",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "expires_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "used_at",
            sa.DateTime(),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_email_verification_tokens_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f("pk_email_verification_tokens"),
        ),
        sa.UniqueConstraint(
            "token_hash",
            name=op.f("uq_email_verification_tokens_token_hash"),
        ),
    )

    op.create_index(
        op.f("ix_email_verification_tokens_user_id"),
        "email_verification_tokens",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    """Remove email verification support."""

    op.drop_index(
        op.f("ix_email_verification_tokens_user_id"),
        table_name="email_verification_tokens",
    )

    op.drop_table("email_verification_tokens")

    op.drop_column(
        "users",
        "email_verified_at",
    )
