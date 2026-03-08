import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config, pool

from alembic import context

# 1. Provide access to the 'app' module by adding project root to sys.path
# This ensures that imports like 'from app.core...' work correctly
sys.path.insert(0, str(Path(__file__).parent.parent))

# 2. Import project-specific infrastructure
# 3. Import models so they register themselves on Base.metadata
import app.models  # noqa: F401 # type: ignore
from app.core.config import settings
from app.database.base import Base

# Alembic Config object - provides access to alembic.ini values
config = context.config

# Setup Python logging using the configuration file defined in alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 4. Link our models' metadata to Alembic for 'autogenerate' support
target_metadata = Base.metadata

# 5. Dynamically set the database URL from our Pydantic settings (.env)
config.set_main_option("sqlalchemy.url", str(settings.DB_URL))


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    Outputs the SQL script to the terminal/file instead of executing it.
    """

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    Connects to the database and applies changes directly.
    """

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# Choose between offline and online execution
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
