from ..models import User
from ..schemas import (
    RegisterRequest,
    UserPasswordChange,
)
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from chat_app.models import (
    UpdateUserError,
    DeleteUserError,
    UserInfoError
)


async def exists(new_user: RegisterRequest, db: AsyncSession) -> bool:
    result = await db.execute(
        select(User).where(User.email == new_user.email),
    )

    user = result.scalars().first()
    if user:
        return True
    return False


async def get_user(request: str, db: AsyncSession) -> User | None:
    query = await db.execute(
        select(User).where(User.id == request),
    )

    user = query.scalars().first()

    if not user:
        return UserInfoError.NOT_EXIST
    return user


async def update_password(request: UserPasswordChange, db: AsyncSession) -> User | UpdateUserError:
    filter_query = (
        User.email == request.email and User.name == request.name)
    query = await db.execute(
        select(User).where(filter_query),
    )

    user = query.scalars().first()
    if not user:
        return UpdateUserError.NOT_EXIST
    if not user.authenticate(request.current_password.get_secret_value()):
        return UpdateUserError.INCORRECT
    user.password_hash = request.fist_password.get_secret_value()
    db.commit()
    db.refresh(user)
    return user


async def delete(id: str, db: AsyncSession) -> User | DeleteUserError:
    filter_query = (
        User.id == id
    )

    query = await db.execute(
        select(User).where(filter_query),
    )

    user = query.scalars().first()
    if not user:
        return DeleteUserError.NOT_EXIST
    db.delete(user)
    db.commit()
    return user