from pydantic import (
    BaseModel,
    Field
)
from typing import (
    Optional,
    List
)
from uuid import UUID
from datetime import datetime
from .common import Pagination

class ConversationCreate(BaseModel):
    user_id: UUID
    title: str = Field(min_length=5, max_length=100)
    model: Optional[str] = Field(min_length=1, max_length=100)
    system_prompt: str = Field(min_length=1, max_length=10000)


class ConversationUpdate(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    model: Optional[str] = Field(min_length=1, max_length=100)


class ConversationPublic(BaseModel):
    id: UUID
    title: str
    model: Optional[str]
    created_at: datetime
    updated_at: datetime
    archived_at: datetime


class ConversationList(BaseModel):
    conversations: List[ConversationPublic]
    pagination: Pagination
