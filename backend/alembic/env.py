import os
import sys
from logging.config import fileConfig
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import pool

from alembic import context

# env.py is at backend/alembic/env.py
ALEMBIC_DIR = Path(__file__).resolve().parent          # backend/alembic
BACKEND_DIR = ALEMBIC_DIR.parent                        # backend/
PROJECT_ROOT = BACKEND_DIR.parent                        # evidence_lens/ (where .env lives)

sys.path.append(str(BACKEND_DIR))          # so `app` is importable
load_dotenv(PROJECT_ROOT / ".env")         # load the REAL .env location

from app.database import Base
from app import models  # noqa: F401  -- registers all models on Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

db_url = (
    f"postgresql+psycopg://{quote_plus(os.getenv('DB_USER'))}:"
    f"{quote_plus(os.getenv('DB_PASSWORD'))}@{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'postgres')}"
)

def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and name in ("spatial_ref_sys",):
        return False
    return True

def run_migrations_offline() -> None:
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        connection=connection,
        include_object=include_object,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(db_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, include_object=include_object,)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()