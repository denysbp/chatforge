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
    list_conversations,
    get_conversation,
    delete_conversation
)
from chat_app.core import DbSession
from fastapi import (
    HTTPException,
    status,
    APIRouter,
    Depends
)
from typing import Annotated
from sqlalchemy.ext.asyncio import (
    AsyncSession
)
from uuid import UUID


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
    db: DbSession
):

    return await create_conversation(request, user, db)


@conversation_route.get(
    "/convesations",
    response_model=ConversationList | list,
    status_code=status.HTTP_200_OK
)
async def get_conversations(
    user: CurrentUser,
    db: DbSession
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


@conversation_route.get(
    "/{c_id}",
    response_model=ConversationPublic,
    status_code=status.HTTP_200_OK
)
async def conversation(
    user: CurrentUser,
    db: DbSession,
    c_id: UUID
):
    conversation = await get_conversation(
        user,
        db,
        c_id
    )
    return conversation


@conversation_route.delete(
    "/{c_id}",
    response_model=ConversationPublic,
    status_code=status.HTTP_200_OK
)
async def delete(
    user: CurrentUser,
    db: DbSession,
    c_id: UUID
):
    conversation = await delete_conversation(
        user,
        db,
        c_id
    )
    return conversation