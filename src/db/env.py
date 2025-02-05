from logging.config import fileConfig
from typing import Literal

from alembic import context
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.sql.schema import SchemaItem

from common.models import Base, Entity
from core.dependencies import get_settings
from core.settings import Settings
from db.alembic_classes import mapper_classes

config = context.config
settings: Settings = get_settings()

alembic_mapper_classes: tuple[type[Entity], ...]
alembic_mapper_classes = mapper_classes
sqlalchemy_url = 'sqlalchemy.url'
config.set_main_option(
    name=sqlalchemy_url,
    value=settings.postgres_url,
)
if config.config_file_name is not None:
    fileConfig(
        fname=config.config_file_name,
    )

target_metadata = Base.metadata


def include_object(
    obj: SchemaItem,
    name: str | None,
    type_: Literal[
        'schema', 'table',
        'column', 'index',
        'unique_constraint',
        'foreign_key_constraint',
    ],
    reflected: bool,
    compare_to: SchemaItem | None,
) -> bool:
    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the
    context with just a URL
    and not an Engine, though
    an Engine is acceptable
    here as well. By skipping
    the Engine creation
    we don't even need a
    DBAPI to be available.

    Calls to context.execute() here
    emit the given string to the
    script output.

    """
    url: str = config.get_main_option(
        name=sqlalchemy_url, default='',
    )
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
        include_object=include_object,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    url: str = config.get_main_option(
        name=sqlalchemy_url, default='',
    )
    connectable: Engine
    connectable = create_engine(url=url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            include_object=include_object,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
