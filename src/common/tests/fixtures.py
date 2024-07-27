from typing import Generator

from pytest import fixture
from sqlalchemy.orm import Session
from sqlalchemy_utils import (
    drop_database,
)
from starlette.testclient import (
    TestClient,
)

from core.dependencies import (
    get_settings,
    get_db, get_cache,
)
from core.main import main_app
from core.settings import Settings
from .dependencies import (
    get_test_settings,
    get_test_db, get_test_cache,
)
from ..clients import RedisClient


@fixture()
def test_settings() -> Settings:
    return get_test_settings()


@fixture()
def test_db(
    test_settings: Settings,
) -> Generator[
    type[Session], None, None,
]:
    yield get_test_db()
    url = test_settings.postgres_url
    drop_database(url=url)


@fixture()
def test_cache(
    test_settings: Settings,
) -> Generator[
    RedisClient, None, None,
]:
    yield get_test_cache()
    url = test_settings.redis_url
    redis_client = RedisClient(
        redis_url=url,
    )
    redis_client.flush_db()


@fixture()
def client() -> TestClient:
    main_app.dependency_overrides = {
        get_settings: get_test_settings,
        get_db: get_test_db,
        get_cache: get_test_cache,
    }
    return TestClient(app=main_app)
