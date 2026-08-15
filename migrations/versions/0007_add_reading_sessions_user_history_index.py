"""Add reading sessions user history index.

Revision ID: 0007
Revises: 0006
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0007"
down_revision: str | None = "0006"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

INDEX_NAME = "ix_reading_sessions_user_started_id"


def upgrade() -> None:
    op.create_index(
        INDEX_NAME,
        "reading_sessions",
        ["user_id", "started_at", "id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(INDEX_NAME, table_name="reading_sessions")
