from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect, text
from tsidpy import TSID

from app.read.domain.value_objects.book_completion_id import BookCompletionId

NOW = "2026-01-01 00:00:00"
COMPLETIONS_TABLE = "book_completions"


def tsid() -> str:
    return TSID.create().to_string()


def migration_config(database_path: Path) -> Config:
    config = Config(str(Path(__file__).resolve().parents[3] / "alembic.ini"))
    config.set_main_option("sqlalchemy.url", f"sqlite:///{database_path.as_posix()}")
    return config


@pytest.fixture
def migration_database(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Config]:
    database_path = tmp_path / "migration.db"
    monkeypatch.setenv("LIFEOS_DATABASE_URL", f"sqlite:///{database_path.as_posix()}")
    return database_path, migration_config(database_path)


def database_connection(database_path: Path) -> sqlite3.Connection:
    database = sqlite3.connect(database_path)
    database.execute("PRAGMA foreign_keys = ON")
    return database


def add_user(database: sqlite3.Connection, user_id: str) -> None:
    database.execute(
        "INSERT INTO users (id, email, hashed_password, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (user_id, f"{user_id}@example.test", "hash", NOW, NOW),
    )


def add_book(
    database: sqlite3.Connection, book_id: str, owner_id: str, total_pages: int = 100
) -> None:
    database.execute(
        """
        INSERT INTO books (
            id, user_id, title, author, total_pages, isbn, publisher, edition,
            cover, genre, language, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            book_id,
            owner_id,
            "Book",
            "Author",
            total_pages,
            None,
            None,
            None,
            None,
            None,
            None,
            NOW,
            NOW,
        ),
    )


def add_session(
    database: sqlite3.Connection,
    session_id: str,
    owner_id: str,
    book_id: str,
    start_page: int,
    end_page: int,
    ended_at: str,
) -> None:
    database.execute(
        """
        INSERT INTO reading_sessions (
            id, user_id, book_id, start_page, end_page, started_at, ended_at,
            notes, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session_id,
            owner_id,
            book_id,
            start_page,
            end_page,
            "2026-01-01 00:00:00",
            ended_at,
            None,
            NOW,
            NOW,
        ),
    )


def completion_rows(database: sqlite3.Connection) -> list[tuple[str, str, str]]:
    return database.execute(
        "SELECT id, book_id, completed_at FROM book_completions ORDER BY book_id"
    ).fetchall()


def completion_state(database: sqlite3.Connection) -> set[tuple[str, datetime]]:
    return {
        (book_id, datetime.fromisoformat(completed_at))
        for _, book_id, completed_at in completion_rows(database)
    }


def source_snapshots(
    database: sqlite3.Connection,
) -> tuple[list[tuple[object, ...]], list[tuple[object, ...]]]:
    return (
        database.execute("SELECT * FROM books ORDER BY id").fetchall(),
        database.execute("SELECT * FROM reading_sessions ORDER BY id").fetchall(),
    )


def test_fresh_upgrade_creates_frozen_completion_schema(
    migration_database: tuple[Path, Config],
) -> None:
    database_path, config = migration_database
    command.upgrade(config, "head")

    engine = create_engine(f"sqlite:///{database_path.as_posix()}")
    with engine.connect() as database:
        inspector = inspect(database)
        assert inspector.has_table(COMPLETIONS_TABLE)
        assert {column["name"] for column in inspector.get_columns(COMPLETIONS_TABLE)} == {
            "id",
            "book_id",
            "completed_at",
            "created_at",
        }
        assert inspector.get_pk_constraint(COMPLETIONS_TABLE)["constrained_columns"] == ["id"]
        assert any(
            constraint["column_names"] == ["book_id"]
            for constraint in inspector.get_unique_constraints(COMPLETIONS_TABLE)
        )
        foreign_key = inspector.get_foreign_keys(COMPLETIONS_TABLE)[0]
        assert foreign_key["constrained_columns"] == ["book_id"]
        assert foreign_key["referred_table"] == "books"
        assert foreign_key["referred_columns"] == ["id"]
        assert foreign_key["options"].get("ondelete") == "RESTRICT"
        assert {
            (index["name"], tuple(index["column_names"]))
            for index in inspector.get_indexes(COMPLETIONS_TABLE)
        } == {("ix_book_completions_completed_at_book_id", ("completed_at", "book_id"))}
        assert database.execute(text("PRAGMA foreign_keys")).scalar_one() == 1
        assert database.execute(text("PRAGMA foreign_key_check")).all() == []
        assert database.execute(text("SELECT COUNT(*) FROM book_completions")).scalar_one() == 0


def test_populated_upgrade_backfills_and_reupgrade_preserves_semantics(
    migration_database: tuple[Path, Config],
) -> None:
    database_path, config = migration_database
    command.upgrade(config, "0007")
    database = database_connection(database_path)
    owner_a, owner_b = tsid(), tsid()
    add_user(database, owner_a)
    add_user(database, owner_b)
    (
        one_session,
        adjacent,
        overlap,
        gap,
        final_gap,
        page_order,
        tied,
        incomplete,
        no_sessions,
        mismatch,
    ) = (tsid(), tsid(), tsid(), tsid(), tsid(), tsid(), tsid(), tsid(), tsid(), tsid())
    for book_id in (
        one_session,
        adjacent,
        overlap,
        gap,
        final_gap,
        page_order,
        tied,
        incomplete,
        no_sessions,
        mismatch,
    ):
        add_book(database, book_id, owner_a)
    add_session(database, tsid(), owner_a, one_session, 1, 100, "2026-01-01 10:00:00")
    add_session(database, tsid(), owner_a, adjacent, 1, 50, "2026-01-02 10:00:00")
    add_session(database, tsid(), owner_a, adjacent, 51, 100, "2026-01-03 10:00:00")
    add_session(database, tsid(), owner_a, overlap, 1, 75, "2026-01-01 10:00:00")
    add_session(database, tsid(), owner_a, overlap, 1, 75, "2026-01-02 10:00:00")
    add_session(database, tsid(), owner_a, overlap, 76, 100, "2026-01-03 10:00:00")
    add_session(database, tsid(), owner_a, gap, 1, 40, "2026-01-01 10:00:00")
    add_session(database, tsid(), owner_a, gap, 60, 100, "2026-01-02 10:00:00")
    add_session(database, tsid(), owner_a, final_gap, 1, 40, "2026-01-01 10:00:00")
    add_session(database, tsid(), owner_a, final_gap, 60, 100, "2026-01-02 10:00:00")
    add_session(database, tsid(), owner_a, final_gap, 41, 59, "2026-01-03 10:00:00")
    add_session(database, tsid(), owner_a, page_order, 51, 100, "2026-01-01 10:00:00")
    add_session(database, tsid(), owner_a, page_order, 1, 50, "2026-01-02 10:00:00")
    first_tie, second_tie = sorted((tsid(), tsid()))
    add_session(database, first_tie, owner_a, tied, 1, 50, "2026-01-04 10:00:00")
    add_session(database, second_tie, owner_a, tied, 51, 100, "2026-01-04 10:00:00")
    add_session(database, tsid(), owner_a, incomplete, 1, 50, "2026-01-01 10:00:00")
    add_session(database, tsid(), owner_b, mismatch, 1, 100, "2026-01-01 10:00:00")
    database.commit()
    books_snapshot, sessions_snapshot = source_snapshots(database)
    database.close()

    command.upgrade(config, "0008")
    database = database_connection(database_path)
    completions = completion_rows(database)
    expected = {
        (one_session, datetime(2026, 1, 1, 10)),
        (adjacent, datetime(2026, 1, 3, 10)),
        (overlap, datetime(2026, 1, 3, 10)),
        (final_gap, datetime(2026, 1, 3, 10)),
        (page_order, datetime(2026, 1, 2, 10)),
        (tied, datetime(2026, 1, 4, 10)),
    }
    assert completion_state(database) == expected
    assert (
        database.execute("SELECT COUNT(DISTINCT created_at) FROM book_completions").fetchone()[0]
        == 1
    )
    assert all(
        len(completion_id) == 13
        and TSID.from_string(completion_id).to_string() == completion_id
        and BookCompletionId.from_value(completion_id).to_persistence() == completion_id
        for completion_id, _, _ in completions
    )
    assert source_snapshots(database) == (books_snapshot, sessions_snapshot)
    assert database.execute("PRAGMA foreign_key_check").fetchall() == []
    database.close()

    command.downgrade(config, "0007")
    database = database_connection(database_path)
    assert (
        database.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name = 'book_completions'"
        ).fetchone()[0]
        == 0
    )
    assert source_snapshots(database) == (books_snapshot, sessions_snapshot)
    assert database.execute("PRAGMA foreign_key_check").fetchall() == []
    assert database.execute("SELECT version_num FROM alembic_version").fetchone() == ("0007",)
    database.close()

    command.upgrade(config, "0008")
    database = database_connection(database_path)
    assert completion_state(database) == expected
    assert source_snapshots(database) == (books_snapshot, sessions_snapshot)
    assert database.execute("PRAGMA foreign_key_check").fetchall() == []
    database.close()


@pytest.mark.parametrize("start_page,end_page", [(90, 110), (101, 101)])
def test_invalid_owner_consistent_source_aborts_before_target_ddl(
    migration_database: tuple[Path, Config], start_page: int, end_page: int
) -> None:
    database_path, config = migration_database
    command.upgrade(config, "0007")
    database = database_connection(database_path)
    owner_id, book_id, session_id = tsid(), tsid(), tsid()
    add_user(database, owner_id)
    add_book(database, book_id, owner_id)
    add_session(
        database, session_id, owner_id, book_id, start_page, end_page, "2026-01-01 10:00:00"
    )
    database.commit()
    source_snapshot = (
        database.execute("SELECT total_pages FROM books WHERE id = ?", (book_id,)).fetchone(),
        database.execute(
            "SELECT start_page, end_page FROM reading_sessions WHERE id = ?", (session_id,)
        ).fetchone(),
    )
    database.close()

    with pytest.raises(ValueError, match="cannot interpret ReadingSession"):
        command.upgrade(config, "0008")

    database = database_connection(database_path)
    assert (
        database.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name = 'book_completions'"
        ).fetchone()[0]
        == 0
    )
    assert source_snapshot == (
        database.execute("SELECT total_pages FROM books WHERE id = ?", (book_id,)).fetchone(),
        database.execute(
            "SELECT start_page, end_page FROM reading_sessions WHERE id = ?", (session_id,)
        ).fetchone(),
    )
    database.close()


def test_restrict_rejects_deleting_completed_book(migration_database: tuple[Path, Config]) -> None:
    database_path, config = migration_database
    command.upgrade(config, "0007")
    database = database_connection(database_path)
    owner_id, book_id = tsid(), tsid()
    add_user(database, owner_id)
    add_book(database, book_id, owner_id)
    add_session(database, tsid(), owner_id, book_id, 1, 100, "2026-01-01 10:00:00")
    database.commit()
    database.close()
    command.upgrade(config, "0008")

    database = database_connection(database_path)
    with pytest.raises(sqlite3.IntegrityError):
        database.execute("DELETE FROM books WHERE id = ?", (book_id,))
    database.rollback()
    database.close()


def test_duplicate_canonical_completion_ids_abort_before_target_ddl(
    migration_database: tuple[Path, Config], monkeypatch: pytest.MonkeyPatch
) -> None:
    database_path, config = migration_database
    command.upgrade(config, "0007")
    database = database_connection(database_path)
    owner_id = tsid()
    first_book, second_book = tsid(), tsid()
    add_user(database, owner_id)
    for book_id in (first_book, second_book):
        add_book(database, book_id, owner_id)
        add_session(database, tsid(), owner_id, book_id, 1, 100, "2026-01-01 10:00:00")
    database.commit()
    source_snapshot = source_snapshots(database)
    database.close()

    duplicate_id = tsid()
    monkeypatch.setattr(TSID, "create", staticmethod(lambda: TSID.from_string(duplicate_id)))

    with pytest.raises(ValueError, match="duplicate Completion IDs"):
        command.upgrade(config, "0008")

    database = database_connection(database_path)
    assert (
        database.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name = 'book_completions'"
        ).fetchone()[0]
        == 0
    )
    assert source_snapshots(database) == source_snapshot
    database.close()
