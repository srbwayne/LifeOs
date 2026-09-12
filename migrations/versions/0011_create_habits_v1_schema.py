"""Create Habits V1 persistence schema.

Revision ID: 0011
Revises: 0010
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0011"
down_revision: str | None = "0010"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "habits",
        sa.Column("id", sa.String(26), nullable=False),
        sa.Column("user_id", sa.String(26), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "id", name="uq_habits_user_id_id"),
        sa.UniqueConstraint("user_id", "name", name="uq_habits_user_name"),
    )

    op.create_table(
        "habit_completions",
        sa.Column("id", sa.String(26), nullable=False),
        sa.Column("user_id", sa.String(26), nullable=False),
        sa.Column("habit_id", sa.String(26), nullable=False),
        sa.Column("record_date", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(
            ["user_id", "habit_id"],
            ["habits.user_id", "habits.id"],
            ondelete="RESTRICT",
            name="fk_habit_completions_owner_habit",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id",
            "habit_id",
            "record_date",
            name="uq_habit_completions_user_habit_record_date",
        ),
    )
    op.create_index(
        "ix_habit_completions_user_record_habit",
        "habit_completions",
        ["user_id", "record_date", "habit_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_habit_completions_user_record_habit",
        table_name="habit_completions",
    )
    op.drop_table("habit_completions")
    op.drop_table("habits")
