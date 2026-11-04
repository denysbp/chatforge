from pydantic import (
    BaseModel,
    EmailStr,
    SecretStr,
    Field
)
from typing import (
    Optional,
    List
)
from uuid import UUID
from datetime import datetime


class SendMessageRequest(BaseModel):
    conversation_id: UUID


class MessagePublic(BaseModel):
    pass


class MessageList(BaseModel):
    pass


class StreamEvent(BaseModel):
    pass