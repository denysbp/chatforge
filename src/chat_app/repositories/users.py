from ..models import User
from ..schemas import (
    RegisterRequest,
    UserPublic,
    UserPasswordChange,
    UserUpdateInfo
)
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from chat_app.models import UpdateError


async def exists(new_user: RegisterRequest, db: AsyncSession) -> bool:
    result = await db.execute(
        select(User).where(User.email == new_user.email),
    )

    user = result.scalars().first()
    if user:
        return True
    return False


async def get_user(request: UserPublic, db: AsyncSession) -> User | None:

    filter_query = (
        User.email == request.email and User.id == request.id)
    query = await db.execute(
        select(User).where(filter_query),
    )

    user = query.scalars().first()

    if not user:
        return None
    return user


async def update(request: UserPasswordChange, db: AsyncSession) -> User | UpdateError:
    filter_query = (
        User.email == request.email and User.name == request.name)
    query = await db.execute(
        select(User).where(filter_query),
    )

    user = query.scalars().first()
    if not user:
        return UpdateError.NOT_EXIST
    if not user.authenticate(request.current_password.get_secret_value()):
        return UpdateError.INCORRECT
    user.password_hash = request.fist_password.get_secret_value()
    db.commit()
    db.refresh(user)
    return user