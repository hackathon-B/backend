from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Enum, Index
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("chats.chat_id", ondelete="CASCADE"), nullable=True)
    sender_type = Column(Enum("user", "ai", name="sender_type"), nullable=False)  # Enumで'user'か'ai'のどちらか
    message_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # リレーション設定
    chat = relationship("Chat", back_populates="messages")
    
    # 複合インデックスの追加（チャットIDと作成日時でのソート・検索の効率化）
    __table_args__ = (
        Index('ix_messages_chat_id_created_at', 'chat_id', 'created_at'),
    )
