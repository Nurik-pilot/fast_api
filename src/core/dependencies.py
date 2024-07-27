from functools import lru_cache

from sqlalchemy.future import (
    create_engine, Engine,
)
from sqlalchemy.orm import (
    sessionmaker, Session,
)

from common.clients import RedisClient
from .settings import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_db() -> type[Session]:
    settings: Settings = get_settings()
    engine: Engine = create_engine(
        url=settings.postgres_url,
        echo=False, future=True,
    )
    return sessionmaker(  # type: ignore[return-value]
        expire_on_commit=False, bind=engine,
    )


def get_cache() -> RedisClient:
    settings: Settings = get_settings()
    return RedisClient(
        redis_url=settings.redis_url,
    )
