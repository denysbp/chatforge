from sqlalchemy import (
    String,
    ForeignKey,
    Enum
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
from datetime import datetime


class Message(Base):

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4()
    )

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id")
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

    created_atcreated_at: Mapped[str] = mapped_column(
        default=datetime.isoformat()
    )

    completed_at: Mapped[str] = mapped_column(
        nullable=True
    )