from pydantic import BaseModel
from pydantic.v1 import Field


class CreateUserRequest(BaseModel):
    username: str = Field(
        min_length=8, max_length=64,
        strip_whitespace=True,
    )
    password: str = Field(
        min_length=8, max_length=64,
        strip_whitespace=True,
    )


class CreateUserResponse(BaseModel):
    access_token: str
