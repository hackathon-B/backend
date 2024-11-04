from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("chats.chat_id"), nullable=False)
    sender_type = Column(Enum("user", "ai", name="sender_type"), nullable=False)  # Enumで'user'か'ai'のどちらか
    message_text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # リレーション設定
    chat = relationship("Chat", back_populates="messages")

