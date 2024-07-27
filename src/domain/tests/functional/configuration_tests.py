from datetime import datetime

from sqlalchemy.orm import (
    Session, load_only,
)

from common.tests.functions import (
    iso_formatted,
)
from domain.models import (
    Configuration,
    ConfigurationSnapshot,
)


def test_configuration(
    test_db: type[Session],
) -> None:
    instance: Configuration
    instance = Configuration()
    model = ConfigurationSnapshot
    session: Session
    with test_db() as session, session.begin():
        session.add(instance=instance)
        snapshots = session.query(
            model,
        )
        snapshots = snapshots.options(
            load_only(
                model.data,
                raiseload=True,
            ),
        )
        ordered = snapshots.order_by(
            model.created_at.desc(),
        )
        snapshot = ordered.first()
    assert isinstance(
        snapshot, ConfigurationSnapshot,
    )
    assert isinstance(
        instance.created_at, datetime,
    )
    assert isinstance(
        instance.updated_at, datetime,
    )
    actual = snapshot.data
    created_at = iso_formatted(
        value=instance.created_at,
    )
    updated_at = iso_formatted(
        value=instance.updated_at,
    )
    expected = {
        'id': instance.pk,
        'created_at': created_at,
        'updated_at': updated_at,
        'is_active': instance.is_active,
    }
    assert actual == expected
