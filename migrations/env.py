from __future__ import annotations

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.auth.infrastructure.persistence.models.password_reset_model import (  # noqa: F401
    PasswordResetTokenModel,
)
from app.auth.infrastructure.persistence.models.session_model import SessionModel  # noqa: F401
from app.auth.infrastructure.persistence.models.user_model import UserModel  # noqa: F401
from app.character.infrastructure.persistence.models.character_model import (  # noqa: F401
    CharacterModel,
)
from app.character.infrastructure.persistence.models.player_model import PlayerModel  # noqa: F401
from app.read.infrastructure.persistence.models.book_completion_model import (  # noqa: F401
    BookCompletionModel,
)
from app.read.infrastructure.persistence.models.book_model import BookModel  # noqa: F401
from app.read.infrastructure.persistence.models.reading_session_model import (  # noqa: F401
    ReadingSessionModel,
)
from app.shared.infrastructure.database import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

database_url = os.getenv("LIFEOS_DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
