from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

# 辞書モデルを定義
class DictionaryModel(Base):
    __tablename__ = "dictionary"

    # プライマリキー
    dictionary_id = Column(Integer, primary_key=True, index=True)

    term = Column(String, nullable=False, unique=True)
    definition = Column(String, nullable=False)
    
    # 外部キー: users.user_id
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # テーブルとのリレーションを定義
    user = relationship("User", back_populates="dictionary")