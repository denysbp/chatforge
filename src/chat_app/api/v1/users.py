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
    update_password as password_update,
    delete,
    get_user
)
from chat_app.models import (
    User,
    UpdateUserError,
    DeleteUserError,
    UserInfoError
)
from chat_app.services.auth_service import (
    oauth2_schema,
    verify_acess_token
)


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

@users.get(
    "/info/{str}",
    response_model=UserPublic,
    status_code=status.HTTP_200_OK
)
async def get_info(id: str, db: Annotated[AsyncSession, Depends(data_base.get_db)]):
    user = await get_user(id, db)
    if isinstance(user, UserInfoError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=user.value
        )
    return user


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


@users.put(
    "/change-password",
    response_model=UserPublic,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_password(request: UserPasswordChange, db: Annotated[AsyncSession, Depends(data_base.get_db)]):
    user = await password_update(request, db)
    if isinstance(user, UpdateUserError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=user.value
        )
    return user


@users.delete(
    "/delete/{str}",
    response_model=UserPublic,
    status_code=status.HTTP_200_OK,
    response_description="User successful deleted"
)
async def delete_user(id: str,  db: Annotated[AsyncSession, Depends(data_base.get_db)]):
    user = await delete(id, db)
    if isinstance(user, DeleteUserError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=user.value
        )
    return user