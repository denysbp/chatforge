from ..models import User
from ..schemas import RegisterRequest
from sqlalchemy.orm import Session
from sqlalchemy import select

def exists(new_user: RegisterRequest, db: Session) -> bool:
    result = db.execute(
        select(User).where(User.email == new_user.email),
    )

    user = result.scalars().first()
    if user:
        return True
    return False