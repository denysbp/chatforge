from pydantic import (
    BaseModel,
    EmailStr,
    SecretStr,
    Field
)
from uuid import UUID


class RegisterRequest(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    email: EmailStr = Field(min_length=1, max_length=100)
    password: SecretStr = Field(min_length=1, max_length=255)


class LoginRequest(BaseModel):
    email: EmailStr = Field(min_length=1, max_length=100)
    password: SecretStr = Field(min_length=1, max_length=255)


class AuthResponse(BaseModel):
    id: UUID
    name: str = Field(min_length=3, max_length=30)
    email: EmailStr
    access_token: str
