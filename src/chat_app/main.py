from fastapi import FastAPI
from chat_app.api.v1 import users
from chat_app.core import data_base
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with data_base.engine.begin() as conn:
        await conn.run_sync(data_base.create_tables)
    yield
    await data_base.close()

app = FastAPI(lifespan=lifespan)

app.include_router(users)