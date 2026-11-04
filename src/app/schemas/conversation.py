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
    page: int = Field(ge=1)
    page_size: int = Field(ge=1)
    total: int = Field(ge=0)
    total_pages: int = Field(ge=0)
