from chat-app.enviroment import settings
from pydantic import (
    EmailStr,
    PostgresDsn,
    SecretStr,
    ValidationError
)
import pytest


def test_mode() -> None:

    with pytest.raises(ValidationError):
        settings.MODE = "build"