from sqlalchemy import (
    String,
    DateTime
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from uuid import uuid4
from .base import Base
from pydantic import EmailStr
from pwdlib import PasswordHash
from datetime import datetime, timezone
from typing import List, TYPE_CHECKING
from .conversation import Conversation

password_hash_setter = PasswordHash.recommended()

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    name: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )
    _password_hash: Mapped[str] = mapped_column(
        String(255)
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False
    )

    chats: Mapped[List["Conversation"]] = relationship(
        back_populates="author"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda : datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        onupdate=datetime.now(timezone.utc)
    )

    @hybrid_property
    def password_hash(self):
        raise Exception("You have been blocked")

    @password_hash.setter
    def password_hash(self, password: str) -> None:
        self._password_hash = password_hash_setter.hash(password)

    def authenticate(self, password) -> bool:
        return password_hash_setter.verify(
            password,
            self._password_hash
        )

    serialize_rules = ('-_password_hash', )
