from datetime import (
    UTC,
    datetime,
    timedelta
)
import jwt
from fastapi.security import OAuth2PasswordBearer
from chat_app.enviroment import settings


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def create_acess_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.ACESS_TOKEN_EXPIRE_MINUTES,
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRECT_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def verify_acess_token(token: str) -> str | None:
    try:
        payload = jwt.decode(
            token,
            settings.SECRECT_KEY.get_secret_value(),
            algorithms=[settings.ALGORITHM],
            options={"require": ["exp", "sub"]}
        )
    except jwt.InvalidTokenError:
        return None
    else:
        return payload.get("sub")