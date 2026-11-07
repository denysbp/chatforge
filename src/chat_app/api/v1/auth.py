from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException,
)
from sqlalchemy import select
from typing import Annotated
from chat_app.models import (
    User,
    UserInfoError
)
from chat_app.enviroment import settings
from chat_app.schemas import AuthResponse, LoginRequest, UserPublic
from chat_app.core import data_base
from chat_app.repositories import get_user_with_form
from chat_app.services import create_acess_token


auth = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@auth.post("/token", response_model=AuthResponse)
async def login_for_acess_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(data_base.get_db)]
):
    user = await get_user_with_form(form_data, db)
    if isinstance(user, UserInfoError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=user.value,
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=settings.ACESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_acess_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    return AuthResponse(access_token=access_token, token_type="bearer")
