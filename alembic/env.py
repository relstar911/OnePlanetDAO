from logging.config import fileConfig

from sqlalchemy import pool
from sqlmodel import SQLModel

from alembic import context
from oneplanet_backend.core.anomaly import AnomalyLog  # noqa: F401
from oneplanet_backend.core.config import DATABASE_URL

# Import all models so SQLModel.metadata is populated
from oneplanet_backend.core.models import (  # noqa: F401
    KPI,
    Alert,
    ProofRequest,
    Proposal,
    User,
    Vote,
)
from oneplanet_backend.core.privacy import AuditLog  # noqa: F401
from oneplanet_backend.core.recovery import GuardianAssignment, RecoveryRequest  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    from sqlalchemy import create_engine

    connect_args = {}
    if DATABASE_URL.startswith("sqlite"):
        connect_args["check_same_thread"] = False

    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool, connect_args=connect_args)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
