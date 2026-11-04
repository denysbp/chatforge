from pydantic import (
    BaseModel,
    EmailStr,
    SecretStr,
    Field
)
from uuid import UUID
from datetime import datetime


class RegisterRequest(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    email: EmailStr = Field(min_length=1, max_length=100)
    password: SecretStr


class LoginRequest(BaseModel):
    email: EmailStr = Field(min_length=1, max_length=100)
    password: SecretStr = Field(min_length=1, max_length=255)


class AuthResponse(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    email: EmailStr
    user_id: UUID
    acess_token: SecretStr


class UserPublic(BaseModel):
    user_id: UUID
    email: EmailStr
    name: str
    created_at: datetime
