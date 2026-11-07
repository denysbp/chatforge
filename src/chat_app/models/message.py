from sqlalchemy import (
    String,
    ForeignKey,
    Enum,
    DateTime,
    Integer,
    UniqueConstraint
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from .base import Base
from .enums import (
    MessageRole,
    MessageStatus
)
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .conversation import Conversation


class Message(Base):

    __tablename__ = "messages"

    __table_args__ = (
        UniqueConstraint(
            "conversation_id",
            "sequence",
            name="uq_message_conversation_sequence"
        ),
    )

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    conversation_id: Mapped[UUID] = mapped_column(
        ForeignKey("conversations.id"),
        nullable=False
    )

    conversation: Mapped["Conversation"] = relationship(
        back_populates="messages"
    )

    role: Mapped[MessageRole] = mapped_column(
        Enum(MessageRole),
        default=MessageRole.ASSISTANT
    )

    content: Mapped[str] = mapped_column(
        String(10000),
        default="Hy say hello to me!",
        nullable=False
    )

    sequence: Mapped[int] = mapped_column(
        nullable=False
    )

    status: Mapped[MessageStatus] = mapped_column(
        Enum(MessageStatus),
        default=MessageStatus.READING
    )

    input_tokens: Mapped[int] = mapped_column(
        default=0,
    )

    output_tokens: Mapped[int] = mapped_column(
        default=0,
    )

    error_code: Mapped[int] = mapped_column(
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda : datetime.now(timezone.utc)
    )

    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )