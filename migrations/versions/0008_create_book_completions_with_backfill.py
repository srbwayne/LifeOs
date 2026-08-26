"""Create book completions with historical backfill.

Revision ID: 0008
Revises: 0007
"""

from __future__ import annotations

import datetime
from collections import defaultdict
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from tsidpy import TSID

revision: str = "0008"
down_revision: str | None = "0007"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BOOK_COMPLETIONS_TABLE = "book_completions"
COMPLETED_AT_BOOK_ID_INDEX = "ix_book_completions_completed_at_book_id"


def _source_tables() -> tuple[sa.TableClause, sa.TableClause]:
    books = sa.table(
        "books",
        sa.column("id", sa.String()),
        sa.column("user_id", sa.String()),
        sa.column("total_pages", sa.Integer()),
    )
    reading_sessions = sa.table(
        "reading_sessions",
        sa.column("id", sa.String()),
        sa.column("user_id", sa.String()),
        sa.column("book_id", sa.String()),
        sa.column("start_page", sa.Integer()),
        sa.column("end_page", sa.Integer()),
        sa.column("ended_at", sa.String()),
    )
    return books, reading_sessions


def _assert_source_schema(bind: sa.Connection) -> None:
    inspector = sa.inspect(bind)
    expected_columns = {
        "books": {"id", "user_id", "total_pages"},
        "reading_sessions": {"id", "user_id", "book_id", "start_page", "end_page", "ended_at"},
    }
    for table_name, columns in expected_columns.items():
        if not inspector.has_table(table_name):
            raise ValueError(f"Migration 0008 requires source table {table_name!r}.")
        actual_columns = {column["name"] for column in inspector.get_columns(table_name)}
        if not columns.issubset(actual_columns):
            raise ValueError(f"Migration 0008 source table {table_name!r} is incompatible.")


def _assert_foreign_key_integrity(bind: sa.Connection) -> None:
    if bind.dialect.name != "sqlite":
        return
    if bind.execute(sa.text("PRAGMA foreign_key_check")).all():
        raise ValueError("Migration 0008 requires clean foreign-key integrity.")


def _as_orderable_datetime(value: object, session_id: str) -> datetime.datetime:
    if not isinstance(value, str):
        raise ValueError(f"Migration 0008 cannot order ReadingSession {session_id!r}.")
    try:
        parsed = datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"Migration 0008 cannot order ReadingSession {session_id!r}.") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return parsed.replace(tzinfo=datetime.timezone.utc)
    return parsed.astimezone(datetime.timezone.utc)


def _completion_candidates(bind: sa.Connection) -> list[tuple[str, datetime.datetime]]:
    books, reading_sessions = _source_tables()
    book_rows = bind.execute(
        sa.select(books.c.id, books.c.user_id, books.c.total_pages).order_by(books.c.id)
    ).mappings()
    sessions_by_book: dict[str, list[dict[str, object]]] = defaultdict(list)
    session_rows = bind.execute(
        sa.select(
            reading_sessions.c.id,
            reading_sessions.c.book_id,
            reading_sessions.c.start_page,
            reading_sessions.c.end_page,
            reading_sessions.c.ended_at,
        ).select_from(
            reading_sessions.join(
                books,
                sa.and_(
                    reading_sessions.c.book_id == books.c.id,
                    reading_sessions.c.user_id == books.c.user_id,
                ),
            )
        )
    ).mappings()
    for row in session_rows:
        sessions_by_book[str(row["book_id"])].append(dict(row))

    candidates: list[tuple[str, datetime.datetime]] = []
    for book in book_rows:
        book_id = str(book["id"])
        total_pages = book["total_pages"]
        if not isinstance(total_pages, int) or total_pages <= 0:
            raise ValueError(f"Migration 0008 cannot interpret Book {book_id!r}.")

        ordered_sessions: list[tuple[datetime.datetime, dict[str, object]]] = []
        for session in sessions_by_book[book_id]:
            session_id = str(session["id"])
            start_page = session["start_page"]
            end_page = session["end_page"]
            if (
                not isinstance(start_page, int)
                or not isinstance(end_page, int)
                or start_page < 1
                or end_page < start_page
                or start_page > total_pages
                or end_page > total_pages
            ):
                raise ValueError(
                    "Migration 0008 cannot interpret ReadingSession "
                    f"{session_id!r} for Book {book_id!r}."
                )
            ordered_sessions.append(
                (_as_orderable_datetime(session["ended_at"], session_id), session)
            )

        intervals: list[tuple[int, int]] = []
        for ended_at, session in sorted(
            ordered_sessions, key=lambda item: (item[0], str(item[1]["id"]))
        ):
            intervals.append((int(session["start_page"]), int(session["end_page"])))
            merged: list[tuple[int, int]] = []
            for start_page, end_page in sorted(intervals):
                if merged and start_page <= merged[-1][1] + 1:
                    merged[-1] = (merged[-1][0], max(merged[-1][1], end_page))
                else:
                    merged.append((start_page, end_page))
            if sum(end_page - start_page + 1 for start_page, end_page in merged) == total_pages:
                candidates.append((book_id, ended_at))
                break
    return candidates


def _prepared_rows(bind: sa.Connection) -> list[dict[str, object]]:
    candidates = _completion_candidates(bind)
    prepared: list[dict[str, object]] = []
    completion_ids: set[str] = set()
    for book_id, completed_at in candidates:
        completion_id = TSID.create().to_string()
        if (
            not isinstance(completion_id, str)
            or TSID.from_string(completion_id).to_string() != completion_id
            or len(completion_id) != 13
            or len(completion_id) > 26
        ):
            raise ValueError("Migration 0008 generated a non-canonical Completion ID.")
        if completion_id in completion_ids:
            raise ValueError("Migration 0008 generated duplicate Completion IDs.")
        completion_ids.add(completion_id)
        prepared.append(
            {
                "id": completion_id,
                "book_id": book_id,
                "completed_at": completed_at,
            }
        )

    migration_created_at = datetime.datetime.now()
    return [{**row, "created_at": migration_created_at} for row in prepared]


def _target_table() -> sa.Table:
    return sa.Table(
        BOOK_COMPLETIONS_TABLE,
        sa.MetaData(),
        sa.Column("id", sa.String(length=26), nullable=False),
        sa.Column("book_id", sa.String(length=26), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("book_id"),
    )


def _assert_target_integrity(bind: sa.Connection) -> None:
    inspector = sa.inspect(bind)
    if not inspector.has_table(BOOK_COMPLETIONS_TABLE):
        raise ValueError("Migration 0008 did not create Completion persistence.")
    columns = {column["name"] for column in inspector.get_columns(BOOK_COMPLETIONS_TABLE)}
    if columns != {"id", "book_id", "completed_at", "created_at"}:
        raise ValueError("Migration 0008 Completion persistence has an unexpected schema.")
    _assert_foreign_key_integrity(bind)


def upgrade() -> None:
    bind = op.get_bind()
    _assert_source_schema(bind)
    _assert_foreign_key_integrity(bind)
    prepared_rows = _prepared_rows(bind)

    target_table = _target_table()
    op.create_table(
        BOOK_COMPLETIONS_TABLE,
        sa.Column("id", sa.String(length=26), nullable=False),
        sa.Column("book_id", sa.String(length=26), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("book_id"),
    )
    op.create_index(
        COMPLETED_AT_BOOK_ID_INDEX,
        BOOK_COMPLETIONS_TABLE,
        ["completed_at", "book_id"],
        unique=False,
    )
    if prepared_rows:
        bind.execute(sa.insert(target_table), prepared_rows)
    _assert_target_integrity(bind)


def downgrade() -> None:
    op.drop_index(COMPLETED_AT_BOOK_ID_INDEX, table_name=BOOK_COMPLETIONS_TABLE)
    op.drop_table(BOOK_COMPLETIONS_TABLE)
