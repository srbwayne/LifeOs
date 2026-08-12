"""Add owner and book index to reading sessions.

Revision ID: 0006
Revises: 0005
Create Date: 2026-08-12 00:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

revision: str = "0006"
down_revision: str | None = "0005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_index(
        "ix_reading_sessions_user_book",
        "reading_sessions",
        ["user_id", "book_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_reading_sessions_user_book",
        table_name="reading_sessions",
    )
