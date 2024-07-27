from returns.result import (
    Failure, Success, Result,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import (
    Session, load_only,
)

from common.schemas import (
    ClientError, ResourceNotFound,
)
from common.sqlalchemy_error_handler import (
    SQLAlchemyErrorHandler,
)
from ..functions import (
    make_password, check_password,
)
from ..models import User
from ..schemas import (
    CreateUserRequest,
    SignInRequest,
    SignInFailure,
)


class UserRepository:
    def __init__(
        self, db: type[Session],
    ) -> None:
        super().__init__()
        self.db = db

    def create(
        self, request: CreateUserRequest,
    ) -> Result[str, ClientError]:
        instance = User(
            username=request.username,
            password=make_password(
                password=request.password,
            ),
        )
        try:
            with (
                self.db() as session,
                session.begin(),
            ):
                session.add(
                    instance=instance,
                )
            return Success(
                inner_value=instance.pk,
            )
        except IntegrityError as exception:
            handler = SQLAlchemyErrorHandler()
            return handler.handle(
                exception=exception,
            )

    def sign_in(
        self, request: SignInRequest,
    ) -> Result[str, ClientError]:
        failure = SignInFailure
        with self.db() as session:
            users = session.query(User)
            users = users.filter_by(
                username=request.username,
            )
            users = users.options(
                load_only(
                    User.id,
                    User.password,
                    raiseload=True,
                ),
            )
            user = users.one_or_none()
        if user is None:
            detail = failure.credentials
            return Failure(
                inner_value=ResourceNotFound(
                    detail=detail,
                ),
            )
        if not check_password(
            raw_password=request.password,
            hashed_password=user.password,
        ):
            detail = failure.credentials
            return Failure(
                inner_value=ClientError(
                    detail=detail,
                ),
            )
        return Success(inner_value=user.pk)
