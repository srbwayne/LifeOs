"""Create books table.

Revision ID: 0004
Revises: 0003
Create Date: 2026-08-09 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0004"
down_revision: str | None = "0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "books",
        sa.Column("id", sa.String(length=26), nullable=False),
        sa.Column("user_id", sa.String(length=26), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("author", sa.String(), nullable=False),
        sa.Column("total_pages", sa.Integer(), nullable=False),
        sa.Column("isbn", sa.String(), nullable=True),
        sa.Column("publisher", sa.String(), nullable=True),
        sa.Column("edition", sa.String(), nullable=True),
        sa.Column("cover", sa.String(), nullable=True),
        sa.Column("genre", sa.String(), nullable=True),
        sa.Column("language", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("total_pages > 0", name="ck_books_total_pages_positive"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_books_user_id", "books", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_books_user_id", table_name="books")
    op.drop_table("books")
