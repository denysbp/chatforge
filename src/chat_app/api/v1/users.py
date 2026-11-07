from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException
)
from src.chat_app.schemas import (
    RegisterRequest,
    UserPublic
)
from sqlalchemy.orm import Session
from typing import Annotated
from src.chat_app.core import data_base
from src.chat_app.repositories import exists
from src.chat_app.models import User

users = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@users.post(
    "/sign-up",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED
)
def create_user(new_user: RegisterRequest, db: Annotated[Session, Depends(data_base.get_db)]):
    if exists(new_user, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email already exists"
        )

    user = User(
        name=new_user.name,
        email=new_user.email
    )
    user.password_hash = new_user.password.get_secret_value()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user