from fastapi import FastAPI
from src.chat_app.api.v1 import users

app = FastAPI()

app.include_router(users)