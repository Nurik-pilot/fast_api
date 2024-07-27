from uuid import uuid4

from httpx import Response
from starlette.testclient import TestClient

from faas.schemas import SignInFailure


def test_profile_200(
    authenticated_client: TestClient,
) -> None:
    response = authenticated_client.get(
        url='/api/users/profile/',
    )
    assert response.status_code == 200
    data = response.json()
    user_id = data['user_id']
    assert isinstance(user_id, str)


def test_profile_401(
    client: TestClient,
) -> None:
    access_token = str(uuid4())
    value = f'Bearer {access_token}'
    client.headers.update(
        {'Authorization': value},
    )
    failure = SignInFailure
    detail = failure.access_token
    expected = {'detail': detail}
    response: Response = client.get(
        url='/api/users/profile/',
    )
    assert response.status_code == 401
    assert response.json() == expected
