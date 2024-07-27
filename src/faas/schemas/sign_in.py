from pydantic import BaseModel
from pydantic.v1 import Field

from common.schemas import AbstractFailure


class SignInRequest(BaseModel):
    username: str = Field(
        min_length=8, max_length=64,
        strip_whitespace=True,
    )
    password: str = Field(
        min_length=8, max_length=64,
        strip_whitespace=True,
    )


class SignInResponse(BaseModel):
    access_token: str


class SignInFailure(
    AbstractFailure,
):
    credentials: str = 'Invalid credentials.'
    access_token: str = 'Invalid access token.'
