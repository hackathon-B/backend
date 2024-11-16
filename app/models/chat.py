from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class Chat(Base):
    __tablename__ = "chats"
    
    # プライマリキー
    chat_id = Column(Integer, primary_key=True, index=True, autoincrement=True)  
    # 外部キー: users.user_id
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    chat_title = Column(String, nullable=False)
    use_model_id = Column(Integer, ForeignKey("ai_models.ai_model_id", ondelete="SET NULL"), nullable=True)
    # 自己参照外部キー: 親チャットのID
    parent_chat_id = Column(Integer, ForeignKey("chats.chat_id", ondelete="CASCADE"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # リレーション設定
    user = relationship("User", back_populates="chats")
    ai_model = relationship("AIModel", back_populates="chats")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan") # チャット削除時にメッセージも削除
    # 自己参照のリレーション
    parent_chat = relationship("Chat", remote_side=[chat_id], backref=relationship("Chat", cascade="all, delete-orphan", name="child_chats"), cascade="all")
    
    # 複合インデックスの追加
    __table_args__ = (
        Index('ix_chats_user_id_created_at', 'user_id', 'created_at'),
    )
    