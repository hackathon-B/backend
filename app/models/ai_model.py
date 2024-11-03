from sqlalchemy import Column, Integer, String
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class AIModel(Base):
    __tablename__ = "ai_models"
    
    ai_model_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ai_model_name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    
    # リレーション設定
    users = relationship("User", back_populates="default_ai_model")
    chats = relationship("Chat", back_populates="ai_model")