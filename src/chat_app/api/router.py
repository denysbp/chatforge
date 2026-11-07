from fastapi import APIRouter
from chat_app.api.v1.users import users


api_router = APIRouter(
    prefix="/api"
)

api_router.include_router(users)