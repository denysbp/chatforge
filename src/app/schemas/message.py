from pydantic import (
    BaseModel,
    Field,
)
from ..models import (
    MessageStatus,
    MessageRole
)
from typing import (
    List
)
from uuid import UUID
from datetime import datetime
from .common import Pagination


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
    pagination: Pagination


class StreamEvent(BaseModel):
    event: str
    data: dict