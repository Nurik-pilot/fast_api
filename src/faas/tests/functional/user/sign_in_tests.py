from httpx import Response
from pytest import mark
from starlette.testclient import TestClient

from faas.models import User
from faas.schemas import SignInFailure


def test_sign_in_200(
    client: TestClient, user: User,
    faas_strings: dict[str, str],
) -> None:
    username = faas_strings['username']
    password = faas_strings['password']
    response: Response = client.post(
        url='/api/users/sign_in/',
        data={
            'username': username,
            'password': password,
        },
    )
    assert 'access_token' in response.json()
    assert response.status_code == 200


@mark.parametrize(
    argnames=(
        'parametrized_username',
        'parametrized_password',
        'expected_status_code',
    ),
    argvalues=(
        (
            'nursultankassym',
            'Qwerty321', 422,
        ),
        (
            'nursultankassym',
            'Qwerty123', 404,
        ),
    ),
    ids=(0, 1,),
)
def test_sign_in_4xx(
    parametrized_username: str,
    parametrized_password: str,
    expected_status_code: int,
    client: TestClient, user: User,
) -> None:
    _ = SignInFailure
    expected_detail = _.credentials
    expected_response = {
        'detail': expected_detail,
    }
    response: Response = client.post(
        url='/api/users/sign_in/',
        data={
            'username': parametrized_username,
            'password': parametrized_password,
        },
    )
    first = expected_response
    assert response.json() == first
    second = expected_status_code
    assert response.status_code == second
