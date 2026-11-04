from pydantic import (
    BaseModel,
    EmailStr,
    SecretStr,
    Field,
)
from ..models import (
    MessageStatus,
    MessageRole
)
from typing import (
    Optional,
    List
)
from uuid import UUID
from datetime import datetime


class SendMessageRequest(BaseModel):
    conversation_id: UUID
    content: str = Field(min_length=1, max_length=10000)
    role: MessageRole


class MessagePublic(BaseModel):
    id: UUID
    content: str
    sequence: int
    role: MessageRole
    status: MessageStatus
    created_at: datetime


class MessageList(BaseModel):
    messages: List[MessagePublic]
    page: int = Field(ge=1)
    page_size: int = Field(ge=1)
    total: int = Field(ge=0)
    total_pages: int = Field(ge=0)


class StreamEvent(BaseModel):
    event: str
    data: dict