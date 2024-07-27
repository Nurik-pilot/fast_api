from os import environ

from sqlalchemy.future import create_engine
from sqlalchemy.orm import (
    Session, sessionmaker,
)
from sqlalchemy_utils import (
    database_exists, create_database,
)

from common.clients import RedisClient
from common.commands.set_database import Command
from core.settings import Settings
from db.alembic_classes import mapper_classes


def get_test_settings() -> Settings:
    worker_name: str = environ.get(
        'PYTEST_XDIST_WORKER', 'gw0',
    )
    digits: list[str]
    digits = [
        char for char
        in worker_name
        if char.isdigit()
    ]
    worker_id: int = int(''.join(digits)) + 1

    """
    https://stackoverflow.com/a/68496454
    """
    redis_db = worker_id % 16
    redis_url = f'redis://redis:6379/{redis_db}'

    postgres_db = f'test_{worker_id}'
    postgres_dsn = 'user:pass@postgres:5432'
    dsn = f'{postgres_dsn}/{postgres_db}'
    postgres_url = f'postgresql://{dsn}'

    environ.update(
        {
            'POSTGRES_URL': postgres_url,
            'REDIS_URL': redis_url,
        },
    )

    return Settings()


def get_test_db() -> type[Session]:
    settings = get_test_settings()
    postgres_url = settings.postgres_url
    create_database(
        url=postgres_url,
    ) if not database_exists(
        url=postgres_url,
    ) else None

    engine = create_engine(
        url=postgres_url,
        echo=False, future=True,
    )
    for mapper_class in mapper_classes:
        mapper_class.metadata.create_all(
            bind=engine,
        )
    db: type[Session]
    db = sessionmaker(  # type: ignore[assignment]
        expire_on_commit=False, bind=engine,
    )
    Command().handle(db=db)
    return db


def get_test_cache() -> RedisClient:
    settings = get_test_settings()
    return RedisClient(
        redis_url=settings.redis_url,
    )
