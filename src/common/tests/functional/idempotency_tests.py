from sqlalchemy.orm import Session

from common.tests.dependencies import (
    get_test_settings, get_test_db,
)
from core.settings import Settings


def test_idempotency(
    test_settings: Settings,
    test_db: type[Session],
) -> None:
    settings = get_test_settings()
    assert test_settings == settings

    db = get_test_db()
    with db(
    ) as session, test_db(
    ) as test_session:
        assert session.bind is not None
        bind = session.bind
        url = bind.engine.url
        assert test_session.bind is not None
        test_bind = test_session.bind
        test_url = test_bind.engine.url
        assert url == test_url
