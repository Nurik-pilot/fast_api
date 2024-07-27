from faas.functions import (
    make_password, check_password,
)
from faas.models import User


def test_user(
    faas_strings: dict[str, str],
) -> None:
    username = faas_strings['username']
    password = faas_strings['password']
    user = User(
        username=username,
        password=make_password(
            password=password,
        ),
    )
    assert check_password(
        raw_password=password,
        hashed_password=user.password,
    ) is True
    assert isinstance(user.pk, str)
