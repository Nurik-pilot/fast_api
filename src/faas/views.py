from fastapi import APIRouter, Depends
from fastapi.security import (
    OAuth2PasswordRequestForm,
)
from returns.result import Result
from sqlalchemy.orm import Session

from common.failure_handler import (
    FailureHandler,
)
from common.schemas import ClientError
from core.dependencies import (
    get_db, get_settings,
)
from core.settings import Settings
from .dependencies import (
    get_current_user_id,
)
from .repositories import (
    UserRepository, JWTRepository,
)
from .schemas import (
    CreateUserRequest,
    CreateUserResponse,
    SignInRequest,
    SignInResponse,
    ProfileResponse,
)

faas_router = APIRouter()


@faas_router.post(
    path='/users/', status_code=201,
    response_model=CreateUserResponse,
)
def create_user(
    request: CreateUserRequest,
    settings: Settings = Depends(
        dependency=get_settings,
    ),
    db: type[Session] = Depends(
        dependency=get_db,
    ),
) -> CreateUserResponse:
    user_id_or_failure = UserRepository(
        db=db,
    ).create(request=request)
    user_id_or_failure.alt(
        function=FailureHandler().handle,
    )
    access_token: str = JWTRepository(
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
    ).obtain_access_token(
        user_id=user_id_or_failure.unwrap(),
    )
    return CreateUserResponse(
        access_token=access_token,
    )


@faas_router.post(
    path='/users/sign_in/', status_code=200,
    response_model=SignInResponse,
)
def sign_in(
    form: OAuth2PasswordRequestForm = Depends(),
    settings: Settings = Depends(
        dependency=get_settings,
    ),
    db: type[Session] = Depends(
        dependency=get_db,
    ),
) -> SignInResponse:
    request: SignInRequest = SignInRequest(
        username=form.username,
        password=form.password,
    )
    user_repository = UserRepository(db=db)
    user_id: Result[str, ClientError]
    user_id = user_repository.sign_in(
        request=request,
    )
    user_id.alt(
        function=FailureHandler().handle,
    )
    access_token: str
    access_token = JWTRepository(
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
    ).obtain_access_token(
        user_id=user_id.unwrap(),
    )
    return SignInResponse(
        access_token=access_token,
    )


@faas_router.get(
    path='/users/profile/',
    status_code=200,
    response_model=ProfileResponse,
)
def profile(
    user_id: str = Depends(
        dependency=get_current_user_id,
    ),
) -> ProfileResponse:
    return ProfileResponse(
        user_id=user_id,
    )
