from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# データベースエンジンを作成
# pool_pre_pingはコネクションが切れた時に再接続するオプション
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# セッションを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
