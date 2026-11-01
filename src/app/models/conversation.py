from .base import Base
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from sqlalchemy import (
    String,
    ForeignKey
)
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Conversation(Base):

    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4()
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    author: Mapped["User"] = relationship(
        back_populates="conversations"
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    model: Mapped[str] = mapped_column(
        String(50),
        default="Quewn0.6b"
    )
    system_prompt: Mapped[str] = mapped_column(
        String(10000),
        default="Hey say something to me"
    )
    created_at: Mapped[str] = mapped_column(
        default=datetime.isoformat()
    )
    updated_at: Mapped[str] = mapped_column(
        nullable=True
    )
    archived_at: Mapped[str] = mapped_column(
        nullable=True
    )