import os
import sqlite3
from contextlib import closing
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy.engine import make_url


@pytest.fixture
def migration_database(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    database_path = (tmp_path / "habits-migration.db").resolve()
    monkeypatch.setenv("LIFEOS_DATABASE_URL", f"sqlite:///{database_path.as_posix()}")
    return database_path


def migration_config(database_path: Path) -> Config:
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", os.environ["LIFEOS_DATABASE_URL"])
    configured_url = config.get_main_option("sqlalchemy.url")
    assert configured_url is not None
    parsed = make_url(configured_url)
    assert parsed.get_backend_name() == "sqlite"
    assert parsed.database is not None
    assert Path(parsed.database).resolve() == database_path
    assert database_path.name != "lifeos.db"
    return config


def test_migration_0011_schema_and_downgrade_are_disposable(
    migration_database: Path,
) -> None:
    config = migration_config(migration_database)
    command.upgrade(config, "0010")
    command.upgrade(config, "head")

    with closing(sqlite3.connect(migration_database)) as connection:
        revision = connection.execute("SELECT version_num FROM alembic_version").fetchone()[0]
        assert revision == "0011"
        tables = {
            row[0]
            for row in connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        }
        assert {"habits", "habit_completions"}.issubset(tables)

        habit_columns = [row[1] for row in connection.execute("PRAGMA table_info('habits')")]
        completion_columns = [
            row[1] for row in connection.execute("PRAGMA table_info('habit_completions')")
        ]
        assert habit_columns == [
            "id",
            "user_id",
            "name",
            "description",
            "active",
            "created_at",
            "updated_at",
        ]
        assert completion_columns == [
            "id",
            "user_id",
            "habit_id",
            "record_date",
            "created_at",
        ]

        habit_indexes = {row[1] for row in connection.execute("PRAGMA index_list('habits')")}
        completion_indexes = {
            row[1] for row in connection.execute("PRAGMA index_list('habit_completions')")
        }
        assert "ix_habit_completions_user_record_habit" in completion_indexes
        assert not any("active" in index for index in habit_indexes)
        schema_sql = connection.execute(
            "SELECT sql FROM sqlite_master WHERE type = 'table' AND name IN (?, ?)",
            ("habits", "habit_completions"),
        ).fetchall()
        schema_text = "\n".join(row[0] for row in schema_sql)
        assert "uq_habits_user_name" in schema_text
        assert "uq_habits_user_id_id" in schema_text
        assert "uq_habit_completions_user_habit_record_date" in schema_text

        completion_foreign_keys = connection.execute(
            "PRAGMA foreign_key_list('habit_completions')"
        ).fetchall()
        assert any(
            row[2] == "users" and row[3] == "user_id" and row[4] == "id"
            for row in completion_foreign_keys
        )
        assert any(
            row[2] == "habits" and row[3] == "user_id" and row[4] == "user_id"
            for row in completion_foreign_keys
        )
        assert any(
            row[2] == "habits" and row[3] == "habit_id" and row[4] == "id"
            for row in completion_foreign_keys
        )

    command.downgrade(config, "0010")
    with closing(sqlite3.connect(migration_database)) as connection:
        assert connection.execute("SELECT version_num FROM alembic_version").fetchone()[0] == "0010"
        tables = {
            row[0]
            for row in connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        }
        assert "habits" not in tables
        assert "habit_completions" not in tables
