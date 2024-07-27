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


class Phone(Entity):
    __tablename__ = 'faas_phones'
    __table_args__ = (
        CheckConstraint(
            sqltext='char_length(number) >= 1',
        ),
    )
    number = Column(
        type_=String(length=16),
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
        back_populates='phones',
    )
