from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from pydantic import BaseModel, Emailstr
from app.db.dictionary_db import fake_dictionary_db  
from app.schemas.dictionary import UpdateDictionary
from typing import List, Optional
import hashlib
import jwt

app = FastAPI()


# 辞書の登録処理
@app.post("/api/dictionary/register")
def register_dictionary(user_id: int, title: str, content: str):
    if not user_id:
        return {"error": "ユーザーIDが必要です"}
    if not title:
        return {"error": "タイトルが必要です"}
    for dictionary in fake_dictionary_db.values():
        if dictionary["title"] == title:
            return {"error": "同じタイトルがすでに存在します"}
    if not content:
        return {"error": "メモの内容を入力してください"}
    new_id = max(fake_dictionary_db.keys(), default=0) + 1
    fake_dictionary_db[new_id] = {
        "user_id": user_id,
        "title": title,
        "content": content
    }
    return {
        "message": "辞書が正常に登録されました",
        "title": title
    }

# 辞書の一覧表示
@app.get("/api/dictionary/list")
def get_dictionary_list():
    dictionaries = []
    for dictionary_id, dictionary in fake_dictionary_db.items():
        dictionaries.append({"id": dictionary_id, "title": dictionary["title"]})
    return dictionaries 

# 辞書の検索処理    
@app.get("/api/dictionary/search")
def dictionary_search(title: str):
    search_results = [
        {"id": dictionary_id, "title": dictionary["title"]}
        for dictionary_id, dictionary in fake_dictionary_db.items()
        if title.lower() in dictionary["title"].lower()
    ]
    if not search_results:
        return {"message": "検索結果に該当するものがありませんでした"}
    return search_results  



# 編集・更新機能
@app.put("/api/dictionary/{dictionary_id}/update")
def update_dictionary(dictionary_id: int, update_data: UpdateDictionary):
    if dictionary_id not in fake_dictionary_db:
        raise HTTPException(status_code=404, detail="指定された辞書が見つかりません")
    if update_data.title:
        fake_dictionary_db[dictionary_id]["title"] = update_data.title
    else:
        raise HTTPException(status_code=400, detail="タイトルを入力してください")
    if update_data.content:
        fake_dictionary_db[dictionary_id]["content"] = update_data.content
    else:
        raise HTTPException(status_code=400, detail="内容を入力してください")
    
    return {"message": "辞書が正常に更新されました", "updated_data": fake_dictionary_db[dictionary_id]}

# 辞書の削除機能
@app.delete("/api/dictionary/{dictionary_id}")
def dictionary_delete(dictionary_id: int):
    if not dictionary_id in fake_dictionary_db:
        raise HTTPException(status_code=404, detail="指定された辞書は存在しません")
    del fake_dictionary_db[dictionary_id]
    return "正常に削除されました"
