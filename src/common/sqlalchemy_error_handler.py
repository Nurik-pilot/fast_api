from re import findall

from psycopg2 import Error
from psycopg2.errorcodes import (
    UNIQUE_VIOLATION,
)
from returns.result import Failure
from sqlalchemy.exc import (
    IntegrityError,
)

from .schemas import ClientError


class Handler:
    def handle(
        self, exception: IntegrityError,
    ) -> Failure:
        raise NotImplementedError


class UniqueHandler(Handler):
    pattern: str = r'\(+(.*?)\)'
    message: str = ' '.join(
        (
            '{field}: {value}',
            'already exists.',
        ),
    )

    def handle(
        self, exception: IntegrityError,
    ) -> Failure:
        """
        DETAIL:
        Key (field)=(value) already exists.
        """
        original: Error = exception.orig
        field: str
        value: str
        field, value = findall(
            pattern=self.pattern,
            string=original.pgerror,
        )
        message: str = self.message.format(
            field=field, value=value,
        )
        return Failure(
            inner_value=ClientError(
                detail=message,
            ),
        )


class SQLAlchemyErrorHandler:
    handlers: dict[
        str, type[Handler],
    ]

    def __init__(self):
        super().__init__()
        self.handlers = {
            UNIQUE_VIOLATION: UniqueHandler,
        }

    def handle(
        self, exception: IntegrityError,
    ) -> Failure:
        if not isinstance(
            exception.orig, Error,
        ):
            raise exception
        code: str = exception.orig.pgcode
        handler: type[Handler] | None
        handler = self.handlers.get(code)
        if handler is None:
            raise exception
        return handler().handle(
            exception=exception,
        )
