from json import load
from pathlib import Path

from pytest import fixture
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from core.settings import Settings
from faas.functions import make_password
from faas.models import User
from faas.repositories import JWTRepository


@fixture(scope='session')
def faas_strings() -> dict[str, str]:
    filepath = '/'.join(
        (
            '/src', 'faas', 'tests',
            'data', 'strings.json',
        ),
    )
    path = Path(filepath)
    with path.open() as file:
        return load(fp=file)


@fixture()
def user(
    faas_strings: dict[str, str],
    test_db: type[Session],
) -> User:
    username = faas_strings['username']
    password = faas_strings['password']
    instance = User(
        username=username,
        password=make_password(
            password=password,
        ),
    )
    with test_db(
        autoflush=True,
    ) as session, session.begin():
        session.add(instance=instance)
    return instance


@fixture()
def authenticated_client(
    client: TestClient, user: User,
    test_settings: Settings,
) -> TestClient:
    access_token = JWTRepository(
        secret_key=test_settings.secret_key,
        algorithm=test_settings.algorithm,
    ).obtain_access_token(user_id=user.pk)
    value = f'Bearer {access_token}'
    client.headers.update(
        {'Authorization': value},
    )
    return client
