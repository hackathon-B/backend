from fastapi import FastAPI
from api.api import api_router
from core.config import settings

# アプリケーションの初期化
app = FastAPI()

# ルーターを追加    
app.include_router(api_router)

# 起動確認用のエンドポイント
@app.get("/", tag=["Health Check"])
async def heakth_check():
    return {"status" : "healthy"}