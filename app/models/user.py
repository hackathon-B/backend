from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.chat import Chat
from app.models.dictionaries import Dictionary

# ユーザーモデルをを定義
class User(Base):
    __tablename__ = "users"

    # ユーザー情報のカラムを定義
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)

    # Googleログイン用のカラムを定義
    google_id = Column(String, unique=True, index=True, nullable=True)
    user_icon = Column(String, nullable=True)

    # ユーザーが使用するデフォルトのAIモデルを定義    
    name = Column(String(30), nullable=True)
    default_model_id = Column(Integer, ForeignKey("ai_models.ai_model_id"), nullable=True)

    # テーブルとのリレーションを定義
    chats = relationship("Chat", back_populates="user", cascade="all, delete-orphan")
    dictionaries = relationship("Dictionary", back_populates="user", cascade="all, delete-orphan")

    # メール・パスワード認証ユーザーかどうかを判定
    def is_password_user(self):
        return self.hashed_password is not None

    # Google認証ユーザーかどうかを判定
    def is_google_user(self):
        return self.google_id is not None

    # ユーザーの表示名を取得
    def get_display_name(self):
        return self.name if self.name else "ゲストユーザー"