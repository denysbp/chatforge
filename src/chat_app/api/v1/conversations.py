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
from chat_app.schemas.common import Pagination
from chat_app.repositories import (
    create_conversation,
    list_conversations
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
async def create(
    request: MinimalCreate,
    user: CurrentUser,
    db: Annotated[AsyncSession, Depends(data_base.get_db)]
):

    return await create_conversation(request, user, db)


@conversation_route.get(
    "/convesations",
    response_model=ConversationList | list,
    status_code=status.HTTP_200_OK
)
async def get_conversations(
    user: CurrentUser,
    db: Annotated[AsyncSession, Depends(data_base.get_db)]
):
    models = await list_conversations(
        user,
        db
    )
    pagination = Pagination(
        total=len(models)
    )
    conversations = ConversationList(
        conversations=models,
        pagination=pagination
    )
    return conversations

