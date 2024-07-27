from datetime import datetime

from httpx import Response
from sqlalchemy.orm import (
    Session, load_only,
)
from starlette.testclient import (
    TestClient,
)

from common.tests.functions import (
    iso_formatted,
)
from faas.functions import check_password
from faas.models import User, UserSnapshot


def test_create_user_201(
    client: TestClient,
    test_db: type[Session],
    faas_strings: dict[str, str],
) -> None:
    username = faas_strings['username']
    password = faas_strings['password']
    response: Response = client.post(
        url='/api/users/',
        json={
            'username': username,
            'password': password,
        },
    )
    data = response.json()
    token = data.get('access_token')
    assert isinstance(token, str)
    with test_db() as db_session:
        users = db_session.query(User).filter_by(
            username=username,
        )
        assert users.count() == 1
        user = users.first()
        user_snapshots = db_session.query(
            UserSnapshot,
        ).options(
            load_only(
                UserSnapshot.data,
                raiseload=True,
            ),
        )
        user_snapshot = user_snapshots.first()
    assert user is not None
    assert user_snapshot is not None
    assert check_password(
        raw_password=password,
        hashed_password=user.password,
    ) is True
    assert isinstance(
        user.created_at, datetime,
    )
    assert isinstance(
        user.updated_at, datetime,
    )
    expected = {
        'id': str(user.pk),
        'username': user.username,
        'password': user.password,
        'is_active': user.is_active,
        'created_at': iso_formatted(
            value=user.created_at,
        ),
        'updated_at': iso_formatted(
            value=user.updated_at,
        ),
    }
    actual = user_snapshot.data
    assert actual == expected


def test_create_user_422(
    client: TestClient, user: User,
    faas_strings: dict[str, str],
) -> None:
    expected_detail = ' '.join(
        (
            'username: 'nursultankassym',
            'already exists.',
        ),
    )
    expected = {
        'detail': expected_detail,
    }
    username = faas_strings['username']
    password = faas_strings['password']
    response: Response = client.post(
        url='/api/users/',
        json={
            'username': username,
            'password': password,
        },
    )
    assert response.json() == expected
    assert response.status_code == 422
