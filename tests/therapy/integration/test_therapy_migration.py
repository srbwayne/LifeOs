import sqlite3
from pathlib import Path

from alembic import command
from alembic.config import Config


def run_migration(tmp_path: Path, monkeypatch, target: str) -> Path:
    database_path = tmp_path / "therapy-migration.db"
    monkeypatch.setenv("LIFEOS_DATABASE_URL", f"sqlite:///{database_path.as_posix()}")
    config = Config("alembic.ini")
    command.upgrade(config, target)
    return database_path


def test_therapy_migration_up_down_up_uses_only_disposable_database(tmp_path, monkeypatch) -> None:
    database_path = run_migration(tmp_path, monkeypatch, "head")

    with sqlite3.connect(database_path) as connection:
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

    config = Config("alembic.ini")
    command.downgrade(config, "0009")
    with sqlite3.connect(database_path) as connection:
        revision = connection.execute("SELECT version_num FROM alembic_version").fetchone()[0]
        tables = {
            row[0]
            for row in connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        }
        assert revision == "0009"
        assert "therapists" not in tables
        assert "therapy_sessions" not in tables

    command.upgrade(config, "head")
    with sqlite3.connect(database_path) as connection:
        assert connection.execute("SELECT version_num FROM alembic_version").fetchone()[0] == "0010"

    assert database_path.name != "lifeos.db"
