from sqlalchemy import select
from chat_app.models import (
    User,
    UserInfoError
)
from sqlalchemy.ext.asyncio import AsyncSession



async def get_user_with_form(form_data: dict, db: AsyncSession):
    result = await db.execute(
        select(User).where(User.email == form_data.username)
    )

    user = result.scalars().first()
    if not user:
        return UserInfoError.NOT_EXIST
    if not user.authenticate(form_data.password):
        return UserInfoError.INCORRECT
    return user