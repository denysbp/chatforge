from ..models import User
from ..schemas import RegisterRequest
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def exists(new_user: RegisterRequest, db: AsyncSession) -> bool:
    result = await db.execute(
        select(User).where(User.email == new_user.email),
    )

    user = result.scalars().first()
    if user:
        return True
    return False