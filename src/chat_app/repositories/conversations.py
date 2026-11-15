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