from pydantic import (
    BaseModel,
    EmailStr,
    SecretStr,
    Field,
    model_validator
)
from uuid import UUID
from datetime import datetime
from typing import Self


class UserPublic(BaseModel):
    id: UUID
    name: str = Field(min_length=3, max_length=30)
    email: EmailStr = Field(min_length=1, max_length=100)
    created_at: datetime


class UserUpdateInfo(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    email: EmailStr = Field(min_length=1, max_length=100)


class UserPasswordChange(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    email: EmailStr = Field(min_length=1, max_length=100)
    current_password: SecretStr = Field(min_length=1, max_length=255)
    fist_password: SecretStr = Field(min_length=1, max_length=255)
    second_password: SecretStr = Field(min_length=1, max_length=255)


    @model_validator(mode="after")
    def check_match_password(self) -> Self:
        if self.fist_password.get_secret_value() != self.second_password.get_secret_value():
            raise ValueError(
                "Passwords do not match!"
            )
        return self