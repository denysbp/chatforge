from pydantic import (
    BaseModel,
    EmailStr,
)
from uuid import UUID
from datetime import datetime


class UserPublic(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    created_at: datetime
