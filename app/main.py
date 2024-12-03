from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.core.config import settings

# アプリケーションの初期化
app = FastAPI(lifespan=None)

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router)

# ヘルスチェック
@app.get("/", tags=["health-check"])
async def health_check():
    return {"status": "healthy"}