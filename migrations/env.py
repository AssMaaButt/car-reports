import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Make sure 'app' is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your Base and engine
from app.db import engine  # your SQLAlchemy engine
from app.db import Base    # if Base is defined in db.py

# Alembic config
config = context.config

# Logging
fileConfig(config.config_file_name)

# Metadata for autogenerate
target_metadata = Base.metadata

# Offline migrations
def run_migrations_offline():
    url = str(engine.url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()

# Online migrations
def run_migrations_online():
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Execute
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
