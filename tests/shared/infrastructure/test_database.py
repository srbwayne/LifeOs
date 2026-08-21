import sqlite3
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, event, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.pool import NullPool

from app.shared.infrastructure.database import _enable_sqlite_foreign_keys


def test_direct_sqlite_engine_enforces_foreign_keys() -> None:
    engine = create_engine("sqlite:///:memory:")
    try:
        with engine.connect() as connection:
            assert connection.execute(text("PRAGMA foreign_keys")).scalar_one() == 1
    finally:
        engine.dispose()


def test_multiple_new_sqlite_connections_enforce_foreign_keys(tmp_path: Path) -> None:
    engine = create_engine(f"sqlite:///{tmp_path / 'multiple-connections.db'}", poolclass=NullPool)
    try:
        foreign_key_states = []
        for _ in range(3):
            with engine.connect() as connection:
                foreign_key_states.append(
                    connection.execute(text("PRAGMA foreign_keys")).scalar_one()
                )

        assert foreign_key_states == [1, 1, 1]
    finally:
        engine.dispose()


def test_sqlite_foreign_key_enforcement_and_integrity_check(tmp_path: Path) -> None:
    engine = create_engine(f"sqlite:///{tmp_path / 'integrity.db'}")
    try:
        with engine.begin() as connection:
            connection.execute(text("CREATE TABLE parent (id INTEGER PRIMARY KEY)"))
            connection.execute(
                text(
                    "CREATE TABLE child ("
                    "id INTEGER PRIMARY KEY, "
                    "parent_id INTEGER NOT NULL REFERENCES parent(id)"
                    ")"
                )
            )

        with pytest.raises(IntegrityError), engine.begin() as connection:
            connection.execute(text("INSERT INTO child (id, parent_id) VALUES (1, 999)"))

        with engine.begin() as connection:
            connection.execute(text("INSERT INTO parent (id) VALUES (1)"))
            connection.execute(text("INSERT INTO child (id, parent_id) VALUES (2, 1)"))

        with engine.connect() as connection:
            assert connection.execute(text("PRAGMA foreign_key_check")).all() == []
    finally:
        engine.dispose()


def test_alembic_online_sqlite_connection_enforces_foreign_keys(tmp_path: Path) -> None:
    observed_foreign_key_states: list[int] = []

    def observe_foreign_keys(dbapi_connection, _connection_record) -> None:
        if isinstance(dbapi_connection, sqlite3.Connection):
            observed_foreign_key_states.append(
                dbapi_connection.execute("PRAGMA foreign_keys").fetchone()[0]
            )

    event.listen(Engine, "connect", observe_foreign_keys)
    try:
        config = Config("alembic.ini")
        config.set_main_option("script_location", str(Path("migrations").resolve()))
        config.set_main_option("sqlalchemy.url", f"sqlite:///{tmp_path / 'alembic.db'}")
        command.upgrade(config, "head")
    finally:
        event.remove(Engine, "connect", observe_foreign_keys)

    assert observed_foreign_key_states
    assert all(state == 1 for state in observed_foreign_key_states)


def test_non_sqlite_connection_does_not_execute_pragma() -> None:
    class NonSqliteConnection:
        def __init__(self) -> None:
            self.cursor_calls = 0

        def cursor(self) -> None:
            self.cursor_calls += 1
            raise AssertionError("non-SQLite connections must not receive a PRAGMA")

    connection = NonSqliteConnection()

    _enable_sqlite_foreign_keys(connection, None)

    assert connection.cursor_calls == 0
