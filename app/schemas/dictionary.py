from pydantic import BaseModel
from typing import List, Optional


# 辞書の新規登録用スキーマ
class DictionaryCreate(BaseModel):
    term: str  # 辞書のタイトル
    definition: str  # 辞書の内容


# 辞書の更新用スキーマ
class DictionaryUpdate(BaseModel):
    term: Optional[str] = None  # タイトル（オプション）
    definition: Optional[str] = None  # 内容（オプション）


# 辞書のデータベースエントリー用スキーマ
class Dictionary(BaseModel):
    id: int  # 辞書ID
    term: str  # タイトル
    definition: str  # 内容
    user_id: int  # ユーザーID（APIのコードに合わせて追加）

    class Config:
        orm_mode = True  # ORMモデルからスキーマへの変換を有効化


# 特定の辞書エントリー用レスポンススキーマ
class DictionaryEntry(BaseModel):
    term: str  # タイトル
    definition: str  # 内容

    class Config:
        orm_mode = True  # ORMモデルからスキーマへの変換を有効化


# 全ての辞書を表すリストレスポンススキーマ
class DictionaryListResponse(BaseModel):
    dictionaries: List[Dictionary]  # 辞書のリスト

    class Config:
        orm_mode = True  # ORMモデルからスキーマへの変換を有効化


# 辞書削除用レスポンススキーマ
class DeleteResponse(BaseModel):
    message: str  # 削除成功メッセージ