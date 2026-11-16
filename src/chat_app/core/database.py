from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from ..enviroment import settings
from ..models import Base
from .. import models
from typing import AsyncGenerator, Annotated
from fastapi import Depends


class DataBase:
    def __init__(self):
        self.engine = create_async_engine(
            settings.DB_URL.encoded_string(),
            pool_pre_ping=True
        )
        self.AsyncSessionLocal = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    def create_tables(self, conn):
        Base.metadata.create_all(bind=conn)

    async def get_db(self) -> AsyncGenerator[AsyncSession]:
        async with self.AsyncSessionLocal() as db:
            yield db

    async def close(self):
        await self.engine.dispose()

data_base = DataBase()
DbSession = Annotated[AsyncSession, Depends(data_base.get_db)]