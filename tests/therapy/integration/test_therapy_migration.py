import os
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy.engine import make_url


@pytest.fixture
def disposable_directory():
    with TemporaryDirectory(prefix="therapy-migration-") as directory:
        yield Path(directory).resolve()


def guarded_config(database_path: Path) -> Config:
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", os.environ["LIFEOS_DATABASE_URL"])
    configured_url = config.get_main_option("sqlalchemy.url")
    assert configured_url is not None
    parsed = make_url(configured_url)
    assert parsed.get_backend_name() == "sqlite"
    assert parsed.database is not None
    resolved_database = Path(parsed.database).resolve()
    assert database_path.is_absolute()
    assert resolved_database == database_path
    assert resolved_database != (Path(__file__).resolve().parents[3] / "lifeos.db").resolve()
    assert database_path.name != "lifeos.db"
    return config


def run_migration(tmp_path: Path, monkeypatch, target: str) -> Path:
    database_path = (tmp_path / "therapy-migration.db").resolve()
    monkeypatch.setenv("LIFEOS_DATABASE_URL", f"sqlite:///{database_path.as_posix()}")
    config = guarded_config(database_path)
    command.upgrade(config, target)
    return database_path


def test_therapy_migration_up_down_up_uses_only_disposable_database(
    disposable_directory, monkeypatch
) -> None:
    database_path = run_migration(disposable_directory, monkeypatch, "head")

    with closing(sqlite3.connect(database_path)) as connection:
        revision = connection.execute("SELECT version_num FROM alembic_version").fetchone()[0]
        tables = {
            row[0]
            for row in connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        }
        assert revision == "0010"
        assert {"therapists", "therapy_sessions"}.issubset(tables)
        therapist_indexes = {
            row[1] for row in connection.execute("PRAGMA index_list('therapists')")
        }
        session_indexes = {
            row[1] for row in connection.execute("PRAGMA index_list('therapy_sessions')")
        }
        assert "ix_therapists_user_name_id" in therapist_indexes
        assert "ix_therapy_sessions_user_occurred_id" in session_indexes
        therapist_fk = connection.execute("PRAGMA foreign_key_list('therapists')").fetchall()
        session_fk = connection.execute("PRAGMA foreign_key_list('therapy_sessions')").fetchall()
        assert any(
            row[2] == "users" and row[3] == "user_id" and row[4] == "id" for row in therapist_fk
        )
        assert any(
            row[2] == "therapists" and row[3] == "user_id" and row[4] == "user_id"
            for row in session_fk
        )
        assert any(
            row[2] == "therapists" and row[3] == "therapist_id" and row[4] == "id"
            for row in session_fk
        )

    config = guarded_config(database_path)
    command.downgrade(config, "0009")
    with closing(sqlite3.connect(database_path)) as connection:
        revision = connection.execute("SELECT version_num FROM alembic_version").fetchone()[0]
        tables = {
            row[0]
            for row in connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        }
        assert revision == "0009"
        assert "therapists" not in tables
        assert "therapy_sessions" not in tables

    command.upgrade(guarded_config(database_path), "head")
    with closing(sqlite3.connect(database_path)) as connection:
        assert connection.execute("SELECT version_num FROM alembic_version").fetchone()[0] == "0010"

    assert database_path.name != "lifeos.db"


def test_migration_guard_rejects_mismatched_target(disposable_directory, monkeypatch) -> None:
    expected = disposable_directory / "therapy-migration.db"
    other = disposable_directory / "other.db"
    monkeypatch.setenv("LIFEOS_DATABASE_URL", f"sqlite:///{other.as_posix()}")

    with pytest.raises(AssertionError):
        guarded_config(expected)

    assert not expected.exists()
    assert not other.exists()
