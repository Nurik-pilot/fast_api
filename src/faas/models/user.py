from typing import TYPE_CHECKING

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Mapped

from common.models import Entity

if TYPE_CHECKING:
    from .email import Email
    from .phone import Phone


class User(Entity):
    __tablename__ = 'faas_users'
    username = Column(
        type_=String(length=128),
        unique=True, nullable=False,
    )
    password: Mapped[str] = Column(
        type_=String(length=128),
        nullable=False,
    )
    emails: Mapped[
        list['Email'],
    ] = relationship(
        argument='Email',
        back_populates='user',
    )
    phones: Mapped[
        list['Phone'],
    ] = relationship(
        argument='Phone',
        back_populates='user',
    )
