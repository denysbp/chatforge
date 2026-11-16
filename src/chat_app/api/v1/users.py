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
from chat_app.repositories import (
    exists,
    update_password as password_update,
    delete,
)
from chat_app.models import (
    User,
    UpdateUserError,
    DeleteUserError,
)
from chat_app.services.auth_service import (
    CurrentUser
)
from chat_app.core import DbSession
from chat_app.services.auth_service import CurrentUser

users = APIRouter(
    prefix="/user",
    tags=["Users"]
)


@users.get(
    "/me",
    response_model=UserPublic,
    status_code=status.HTTP_200_OK
)
async def get_current_user(
    user: CurrentUser,
):
    return user


@users.post(
    "/sign-up",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED
)
async def create_user(request: RegisterRequest, db: DbSession):
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


@users.put(
    "/change-password",
    response_model=UserPublic,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_password(
    request: UserPasswordChange,
    db: DbSession
):
    user = await password_update(request, db)
    if isinstance(user, UpdateUserError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=user.value
        )
    return user


@users.delete(
    "/delete",
    response_model=UserPublic,
    status_code=status.HTTP_200_OK,
    response_description="User successful deleted"
)
async def delete_user(
    user: CurrentUser,
    db: DbSession
):
    user = await delete(user, db)
    if isinstance(user, DeleteUserError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=user.value
        )
    return user