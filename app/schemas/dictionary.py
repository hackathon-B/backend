from pydantic import BaseModel

# 更新用のリクエストデータ構造を定義
class UpdateDictionary(BaseModel):
    title: str
    content: str