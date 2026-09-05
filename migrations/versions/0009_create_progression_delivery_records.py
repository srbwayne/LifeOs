"""Create durable ReadingSession to Logos delivery records.

Revision ID: 0009
Revises: 0008
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0009"
down_revision: str | None = "0008"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "progression_delivery_records",
        sa.Column("id", sa.String(26), nullable=False),
        sa.Column("reading_session_id", sa.String(26), nullable=False),
        sa.Column("source", sa.String(64), nullable=False),
        sa.Column("idempotency_key", sa.String(255), nullable=False),
        sa.Column("subject_namespace", sa.String(64), nullable=False),
        sa.Column("subject_external_id", sa.String(255), nullable=False),
        sa.Column("configuration_key", sa.String(255), nullable=False),
        sa.Column("configuration_revision", sa.Integer(), nullable=False),
        sa.Column("pages_read", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(16), nullable=False, server_default="PENDING"),
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("last_attempt_at", sa.DateTime(), nullable=True),
        sa.Column("delivered_at", sa.DateTime(), nullable=True),
        sa.Column("last_error", sa.String(500), nullable=True),
        sa.ForeignKeyConstraint(
            ["reading_session_id"], ["reading_sessions.id"], ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("reading_session_id", name="uq_progression_delivery_session"),
        sa.UniqueConstraint(
            "source", "idempotency_key", name="uq_progression_delivery_identity"
        ),
        sa.CheckConstraint(
            "status IN ('PENDING', 'DELIVERED', 'FAILED')",
            name="ck_progression_delivery_status",
        ),
        sa.CheckConstraint(
            "attempt_count >= 0",
            name="ck_progression_delivery_attempt_count_nonnegative",
        ),
    )
    op.create_index(
        "ix_progression_delivery_status_created",
        "progression_delivery_records",
        ["status", "created_at"],
    )
    op.create_index(
        "ix_progression_delivery_subject_created",
        "progression_delivery_records",
        ["subject_namespace", "subject_external_id", "created_at", "id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_progression_delivery_subject_created",
        table_name="progression_delivery_records",
    )
    op.drop_index(
        "ix_progression_delivery_status_created",
        table_name="progression_delivery_records",
    )
    op.drop_table("progression_delivery_records")
