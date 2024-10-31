from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class Chat(Base):
    __tablename__ = "chats"
    
    # プライマリキー
    chat_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # 外部キー: users.user_id
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    
    # チャットのタイトル
    chat_title = Column(String, nullable=False)
    
    # 外部キー ai_models.ai_model_id
    use_model_id = Column(Integer, ForeignKey("ai_models.ai_model_id"), nullable=True)
    
    # 自己参照外部キー: 親チャットのID
    parent_chat_id = Column(Integer, ForeignKey("chats.chat_id"), nullable=True)
    
    # 作成日時
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 更新日時
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # リレーション設定
    user = relationship("User", back_populates="chats")
    ai_model = relationship("AIModel", back_populates="chats")
    parent_chat = relationship("Chat", remote_side=[chat_id], backref="child_chats")
    