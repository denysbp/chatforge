from chat_app.models import Conversation
from chat_app.schemas import (
    ConversationCreate,
    ConversationList,
    ConversationPublic,
    ConversationUpdate,
    MinimalCreate
)
from chat_app.models import User
from sqlalchemy.ext.asyncio import (
    AsyncSession
)
from sqlalchemy import (
    select
)
from typing import (
    List
)
from fastapi import (
    HTTPException,
    status
)
from uuid import UUID


async def create_conversation(
    request: MinimalCreate,
    user: User,
    db: AsyncSession
) -> Conversation:
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


async def list_conversations(
    user: User,
    db: AsyncSession
) -> List[ConversationPublic]:
    query = await db.execute(select(Conversation).where(
            Conversation.user_id == user.id
        )
    )

    conversations = query.scalars().all()
    models = [
        ConversationPublic(
            id=c.id,
            title=c.title,
            model=c.model,
            created_at=c.created_at
        ) for c in conversations
    ]

    return models


async def get_conversation(
    user: User,
    db: AsyncSession,
    c_id: UUID,
) -> Conversation:
    query = await db.execute(
        select(Conversation).where(Conversation.id == c_id)
    )

    conversation = query.scalars().first()
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation: {c_id} not found."
        )
    elif conversation.user_id != user.id:
        error = "You don't have access to that conversation."
        error += "It seems you're not the owner,ask the owner to send you a link."
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error
        )
    return conversation


async def delete_conversation(
    user: User,
    db: AsyncSession,
    c_id: UUID,
) -> Conversation:
    query = await db.execute(
        select(Conversation).where(Conversation.id == c_id)
    )

    conversation = query.scalars().all()
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation: {c_id} not found."
        )

    elif conversation.user_id != user.id:
        error = "You don't have permission to delete that conversation."
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error
        )

    db.delete(conversation)
    db.commit()
    return conversation