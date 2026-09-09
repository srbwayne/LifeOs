"""Create Therapy V1 persistence schema.

Revision ID: 0010
Revises: 0009
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0010"
down_revision: str | None = "0009"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "therapists",
        sa.Column("id", sa.String(26), nullable=False),
        sa.Column("user_id", sa.String(26), nullable=False),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "id", name="uq_therapists_user_id_id"),
    )
    op.create_index(
        "ix_therapists_user_name_id",
        "therapists",
        ["user_id", "name", "id"],
    )

    op.create_table(
        "therapy_sessions",
        sa.Column("id", sa.String(26), nullable=False),
        sa.Column("user_id", sa.String(26), nullable=False),
        sa.Column("therapist_id", sa.String(26), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("private_note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(
            ["user_id", "therapist_id"],
            ["therapists.user_id", "therapists.id"],
            ondelete="RESTRICT",
            name="fk_therapy_sessions_owner_therapist",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_therapy_sessions_user_occurred_id",
        "therapy_sessions",
        ["user_id", "occurred_at", "id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_therapy_sessions_user_occurred_id",
        table_name="therapy_sessions",
    )
    op.drop_table("therapy_sessions")
    op.drop_index("ix_therapists_user_name_id", table_name="therapists")
    op.drop_table("therapists")
