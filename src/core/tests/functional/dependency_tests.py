from sqlalchemy import text

from common.clients import RedisClient
from core.dependencies import (
    get_settings,
    get_db, get_cache,
)
from core.settings import Settings


def test_settings() -> None:
    settings = get_settings()
    assert isinstance(settings, Settings)


def test_db() -> None:
    db = get_db()
    with db() as session:
        cursor = session.execute(
            statement=text(
                text='select 1;',
            ),
        )
        response = cursor.fetchone()
    assert response == (1,)


def test_cache() -> None:
    cache = get_cache()
    assert isinstance(cache, RedisClient)
