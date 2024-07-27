from typing import TYPE_CHECKING

from sqlalchemy import (
    Column, String,
    CheckConstraint,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import (
    UUID,
)
from sqlalchemy.orm import (
    relationship, Mapped,
)

from common.models import Entity

if TYPE_CHECKING:
    from .user import User

regex = '+'.join(
    (
        '^[A-Za-z0-9._+%-]',
        '@[A-Za-z0-9.-]',
        '[.][A-Za-z]+$',
    ),
)

email_regex = f"'{regex}'"


class Email(Entity):
    __tablename__ = 'faas_emails'
    __table_args__ = (
        CheckConstraint(
            sqltext=f'address ~* {email_regex}',
        ),
    )
    address = Column(
        type_=String(length=64),
        nullable=False,
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey(
            column='faas_users.id',
            ondelete='CASCADE',
        ),
    )
    user: Mapped['User'] = relationship(
        argument='User',
        back_populates='emails',
    )
