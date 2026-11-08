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
    ForeignKey,
    DateTime,
    Index
)
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .user import User
    from .message import Message

class Conversation(Base):

    __tablename__ = "conversations"

    __table_args__ = (
        Index(
            "idx_conversation_user_updated",
            "user_id",
            "updated_at"
        ),
    )

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid4
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    author: Mapped["User"] = relationship(
        back_populates="chats"
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    messages: Mapped[List["Message"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan"
    )

    model: Mapped[str] = mapped_column(
        String(50),
        default="Quewn0.6b"
    )
    system_prompt: Mapped[str] = mapped_column(
        String(10000),
        default="Hey say something to me"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone.utc),
        nullable=False,
        default=lambda : datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone.utc),
        nullable=True,
        onupdate=datetime.now(timezone.utc)
    )
    archived_at: Mapped[str] = mapped_column(
        nullable=True
    )