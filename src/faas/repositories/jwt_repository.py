from datetime import (
    datetime, timedelta, UTC,
)

from jwt import (
    encode, decode, PyJWTError,
)
from returns.result import (
    Result, Success, Failure,
)

from ..schemas import SignInFailure


class JWTRepository:
    def __init__(
        self, secret_key: str,
        algorithm: str,
    ) -> None:
        super().__init__()
        self.secret_key = secret_key
        self.algorithm: str = algorithm

    def obtain_access_token(
        self, user_id: str,
        expires_in: int = 86400,
    ) -> str:
        """
        :param user_id:
        :param expires_in: ttl for
        token in seconds
        :return:
        """
        delta = timedelta(minutes=expires_in)
        now = datetime.now(tz=UTC)
        expires_at: datetime = now + delta
        payload: dict[str, str | datetime] = {
            'sub': user_id, 'exp': expires_at,
        }
        return encode(
            payload=payload,
            key=self.secret_key,
            algorithm=self.algorithm,
        )

    def user_id_from_access_token(
        self, access_token: str,
    ) -> Result[str, str]:
        try:
            payload = decode(
                jwt=access_token,
                key=self.secret_key,
                algorithms=[
                    self.algorithm,
                ],
            )
        except PyJWTError:
            failure = SignInFailure
            detail = failure.access_token
            return Failure(
                inner_value=detail,
            )
        return Success(
            inner_value=payload['sub'],
        )
