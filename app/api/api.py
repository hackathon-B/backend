from fastapi import APIRouter

from app.api.endpoints import auth, chats, messages, auth_google, dictionary, user

api_router = APIRouter()

# 各エンドポイントモジュールのルーターをインクルード
api_router.include_router(auth.router, prefix="/api/auth", tags=["auth"])
api_router.include_router(auth_google.router, prefix="/api/auth/google", tags=["auth"])
api_router.include_router(chats.router, prefix="/api/chats", tags=["chats"])
api_router.include_router(messages.router, prefix="/api/chats/{chat_id}/messages", tags=["messages"])
api_router.include_router(dictionary.router, prefix="/api/dictionary", tags=["dictionary"])
api_router.include_router(user.router, prefix="/api/users", tags=["users"])