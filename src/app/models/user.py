from sqlalchemy import (
    String
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
from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .conversation import Conversation

password_hash = PasswordHash.recommended()

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4()
    )
    name: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        EmailStr,
        unique=True
    )
    _password_hash: Mapped[str] = mapped_column(
        String(255)
    )

    is_ative: Mapped[bool] = mapped_column(
        default=True,
        nullable=False
    )

    conversations: Mapped[List["Conversation"]] = relationship(
        back_populates="author"
    )

    created_at: Mapped[str] = mapped_column(
        default=datetime.isoformat()
    )

    updated_at: Mapped[str] = mapped_column(
        nullable=True
    )

    @hybrid_property
    def password_hash(self):
        raise Exception("You have been blocked")

    @password_hash.setter
    def set_password(self, password: str) -> None:
        self._password_hash = password_hash.hash(password)

    def authenticate(self, password) -> bool:
        return password_hash.verify(
            password,
            self._password_hash
        )

    serialize_rules = ('-_password_hash', )
