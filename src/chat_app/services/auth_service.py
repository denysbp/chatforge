from datetime import (
    UTC,
    datetime,
    timedelta
)
import jwt
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import (
    Depends,
    HTTPException,
    status
)
from sqlalchemy import(
    select
)
from sqlalchemy.ext.asyncio import AsyncSession
from chat_app.enviroment import settings
from chat_app.core import data_base
from chat_app.models import (
    RefreshToken,
    UserInfoError,
    User
)
from chat_app.repositories import get_user


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


async def get_loged_user(
    token: Annotated[str, Depends(oauth2_schema)],
    db: Annotated[AsyncSession, Depends(data_base.get_db)]
):
    user_id = verify_acess_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = await get_user(user_id, db)
    if isinstance(user, UserInfoError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=user.value
        )
    return user

CurrentUser = Annotated[User, Depends(get_loged_user)] # FOR CREATE POST AND CONVERSATION