from fastapi import (
    FastAPI,
    HTTPException,
    status,
    APIRouter,
    Depends
)
from typing import Annotated
from sqlalchemy.ext.asyncio import (
    AsyncSession
)
from chat_app.services.auth_service import CurrentUser
from chat_app.core import data_base
from chat_app.models import Conversation
from chat_app.schemas import (
    ConversationCreate,
    ConversationPublic,
    ConversationList,
    ConversationUpdate,
    MinimalCreate
)


conversation_route = APIRouter(
    prefix="/c",
    tags=["Conversations"]
)


@conversation_route.post(
    "/create",
    response_model=ConversationPublic,
    status_code=status.HTTP_201_CREATED
)
async def create_conversation(
    request: MinimalCreate,
    user: CurrentUser,
    db: Annotated[AsyncSession, Depends(data_base.get_db)]
):
    creation = ConversationCreate(
        title=request.title,
        model=request.model,
        system_prompt=request.system_prompt,
        user_id=user.id,
    )
    post = Conversation(
        title=creation.title,
        model=creation.model,
        system_prompt=creation.system_prompt,
        user_id=creation.user_id
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post