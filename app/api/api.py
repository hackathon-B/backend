from fastapi import APIRouter

from app.api.endpoints import auth, chats, messages, auth_google # dictionary

api_router = APIRouter()

# 各エンドポイントモジュールのルーターをインクルード
api_router.include_router(auth.router, prefix="/api/auth", tags=["auth"])
api_router.include_router(auth_google.router, prefix="/api/auth/google", tags=["auth"])
api_router.include_router(chats.router, prefix="/api/chats", tags=["chats"])
api_router.include_router(messages.router, prefix="/api/messages", tags=["messages"])
# dictionary関連のルーターをコメントアウト
# api_router.include_router(dictionary.router, prefix="/api/dictionary", tags=["dictionary"])


