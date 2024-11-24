from pydantic import BaseModel
from typing import List, Optional

class DictionaryBase(BaseModel):
    term: str
    definition: str

class DictionaryCreate(DictionaryBase):
    pass

class UpdateDictionary(BaseModel):
    term: Optional[str] = None
    definition: Optional[str] = None

class Dictionary(DictionaryBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True  # Pydantic v2 以降で orm_mode の代わりに使用

# 辞書リストのスキーマ
class DictionaryList(BaseModel):
    dictionaries: List[Dictionary]  # List 型で Dictionary を含む