from bcrypt import (
    hashpw, gensalt, checkpw,
)


def make_password(password: str) -> str:
    return hashpw(
        password=password.encode(),
        salt=gensalt(),
    ).decode()


def check_password(
    raw_password: str,
    hashed_password: str,
) -> bool:
    return checkpw(
        password=raw_password.encode(),
        hashed_password=hashed_password.encode(),
    )
