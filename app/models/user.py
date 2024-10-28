from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

# モデルクラスを定義
class User(Base):
    __tablename__ = "users"

    # カラムを定義
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
