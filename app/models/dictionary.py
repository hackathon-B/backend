from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Dictionary(Base):
    __tablename__ = "dictionaries"  # テーブル名を小文字・複数形に変更

    # 辞書のID
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # ユーザーID（外部キー）
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)

    # タイトル（最大255文字）
    term = Column(String(255), nullable=False, index=True)

    # 辞書の内容
    definition = Column(Text, nullable=False)

    # リレーション設定（ユーザーと紐付け）
    user = relationship("User", back_populates="dictionaries")

    # 複合インデックスの追加
    __table_args__ = (
        Index("ix_term_user_id", "term", "user_id", unique=True),  # ユーザーごとのタイトル重複を防止
    )