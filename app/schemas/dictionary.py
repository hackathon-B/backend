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
        from_attributes = True 
# 辞書リストのスキーマ
class DictionaryList(BaseModel):
    dictionaries: List[Dictionary] 