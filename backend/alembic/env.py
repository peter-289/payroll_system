# backend/alembic/env.py
import sys
from pathlib import Path

# THIS IS THE EXACT LINE THAT MADE YOUR test_import.py WORK
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# Now these imports work 100%
from backend.config import DATABASE_URL
from backend.database_setups.database_setup import Base, engine

# ------------------- Standard Alembic code below -------------------
from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context

# Alembic Config object
config = context.config

# IMPORTANT: Tell Alembic to use your DATABASE_URL
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# For autogenerate
target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()