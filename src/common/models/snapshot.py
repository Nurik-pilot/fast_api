from uuid import uuid4

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import (
    JSONB, UUID,
)
from sqlalchemy.sql.functions import now

from .base import Base


class Snapshot(Base):
    __abstract__ = True
    id = Column(  # noqa: A003, VNE003
        type_=UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    created_at = Column(
        type_=DateTime(timezone=True),
        default=now(),
        server_default=now(),
        nullable=False,
    )
    snapshot_type = Column(
        type_=String(length=128),
        nullable=False,
    )
    data = Column(
        type_=JSONB(),
        default=dict,
        nullable=False,
    )
