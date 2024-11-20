from fastapi import FastAPI
from app.api.api import api_router
from app.core.config import settings

# アプリケーションの初期化
app = FastAPI()

app.include_router(api_router)

@app.get("/", tags=["health-check"])
async def health_check():
    return {"status": "healthy"}