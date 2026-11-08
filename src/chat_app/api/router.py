from fastapi import APIRouter
from chat_app.api.v1.users import users
from chat_app.api.v1.auth import auth
from chat_app.api.v1.conversations import conversation_route

api_router = APIRouter(
    prefix="/api"
)
api_router.include_router(auth)
api_router.include_router(users)
api_router.include_router(conversation_route)