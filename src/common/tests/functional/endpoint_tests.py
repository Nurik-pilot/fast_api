from httpx import Response
from sqlalchemy.orm import Session
from starlette.testclient import (
    TestClient,
)

from common.clients import RedisClient


def test_client_404(
    client: TestClient,
) -> None:
    response: Response = client.get(
        url='/api/',
    )
    assert response.status_code == 404
    assert response.json() == {
        'detail': 'Not Found',
    }


def test_openapi_200(
    client: TestClient,
) -> None:
    response: Response = client.get(
        url='/openapi.json',
    )
    assert response.status_code == 200
    expected: dict[
        str, str | dict[str, str],
    ]
    expected = {
        'openapi': '3.1.0', 'info': {
            'title': 'seed',
            'version': '0.1.0',
        },
    }
    data: dict[
        str, str | dict[str, str],
    ]
    data = response.json()
    for key, value in expected.items():
        assert data.get(key) == value


def test_state_200(
    test_db: type[Session],
    test_cache: RedisClient,
    client: TestClient,
) -> None:
    response: Response = client.get(
        url='/api/state/',
    )
    assert response.status_code == 200
    assert response.json() == {
        'database_works': True,
        'cache_works': True,
        'broker_works': True,
    }
