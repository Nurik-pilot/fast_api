from fastapi import (
    Depends, HTTPException,
)
from fastapi.security import (
    OAuth2PasswordBearer,
)
from returns.pipeline import is_successful
from returns.result import Result

from core.dependencies import get_settings
from core.settings import Settings
from .repositories import JWTRepository

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/api/users/sign_in/',
)


def get_current_user_id(
    settings: Settings = Depends(
        dependency=get_settings,
    ),
    access_token: str = Depends(
        dependency=oauth2_scheme,
    ),
) -> str:
    user_id: Result[str, str]
    user_id = JWTRepository(
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
    ).user_id_from_access_token(
        access_token=access_token,
    )
    if not is_successful(container=user_id):
        raise HTTPException(
            status_code=401,
            detail=user_id.failure(),
            headers={
                'WWW-Authenticate': 'Bearer',
            },
        )
    return user_id.unwrap()
