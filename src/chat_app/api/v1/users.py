from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException
)
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler
)
from chat_app.schemas import (
    RegisterRequest,
    UserPublic,
    UserPasswordChange
)
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from chat_app.core import data_base
from chat_app.repositories import (
    exists,
    update
)
from chat_app.models import (
    User,
    UpdateError
)

users = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@users.post(
    "/sign-up",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED
)
async def create_user(request: RegisterRequest, db: Annotated[AsyncSession, Depends(data_base.get_db)]):
    if await exists(request, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email already exists"
        )

    user = User(
        name=request.name,
        email=request.email
    )
    user.password_hash = request.password.get_secret_value()
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@users.post(
    "/change-password",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED
)
async def update_password(request: UserPasswordChange, db: Annotated[AsyncSession, Depends(data_base.get_db)]):
    user = await update(request, db)
    if isinstance(user, UpdateError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=user.value
        )
    return user