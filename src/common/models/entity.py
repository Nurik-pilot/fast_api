from typing import Any
from uuid import uuid4

from sqlalchemy import (
    Column, DateTime, Boolean, true,
)
from sqlalchemy.dialects.postgresql import (
    UUID,
)
from sqlalchemy.sql.functions import now

from .base import Base


class Entity(Base):
    __abstract__ = True

    id = Column(  # noqa: A003, VNE003
        type_=UUID(as_uuid=True),
        primary_key=True, default=uuid4,
    )
    created_at = Column(
        type_=DateTime(timezone=True),
        default=now(), nullable=False,
        server_default=now(),
    )
    updated_at = Column(
        type_=DateTime(timezone=True),
        default=now(), server_default=now(),
        onupdate=now(), nullable=False,
    )
    is_active = Column(
        type_=Boolean(),
        server_default=true(),
        default=True, nullable=False,
    )

    def __init__(
        self, **kwargs: Any,
    ) -> None:
        """
        it's here to not have
        pycharm warnings about
        unexpected arguments
        """
        super().__init__(**kwargs)

    @property
    def pk(self) -> str:
        return str(self.id)
