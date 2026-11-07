from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)
from pydantic import (
    PostgresDsn,
    EmailStr,
    SecretStr,
    Field
)
from typing import (
    Annotated,
    Literal
)

class Settings(BaseSettings):
    OPENIA_API: SecretStr
    ADMIN_LOGIN: str
    ADMIN_PASSWORD: SecretStr
    PORT: Annotated[int, Field(ge=1, le=65535)] = 8000
    MODE: Literal["development", "production"]
    ADMIN_EMAIL: EmailStr
    DB_NAME: str
    DB_PASSWORD: SecretStr
    DB_URL: PostgresDsn
    DB_PORT: Annotated[int, Field(ge=1, le=65535)] = 5432
    DB_HOST: str = "localhost"
    SECRECT_KEY: SecretStr
    ACESS_TOKEN_EXPIRE_MINUTES: int
    DB_USER: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        validate_assignment=True
    )

settings = Settings()

if __name__ == "__main__":
    print(settings)