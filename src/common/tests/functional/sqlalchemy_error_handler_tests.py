from pytest import raises
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from common.sqlalchemy_error_handler import (
    SQLAlchemyErrorHandler, Handler,
)
from faas.models import User


def test_sqlalchemy_error_handler(
    test_db: type[Session],
    faas_strings: dict[str, str],
) -> None:
    password = faas_strings['password']
    handler = SQLAlchemyErrorHandler()
    instance = User(
        username=None, password=password,
    )
    try:
        with test_db(
        ) as session, session.begin():
            session.add(instance=instance)
    except IntegrityError as exception:
        with raises(
            expected_exception=IntegrityError,
        ):
            handler.handle(exception=exception)


def test_handler() -> None:
    with raises(
        expected_exception=NotImplementedError,
    ):
        Handler().handle(
            exception=IntegrityError(
                statement='', params={},
                orig=Exception(),
            ),
        )


def test_handler_exception() -> None:
    with raises(
        expected_exception=IntegrityError,
    ):
        SQLAlchemyErrorHandler().handle(
            exception=IntegrityError(
                statement='', params={},
                orig=Exception(),
            ),
        )
