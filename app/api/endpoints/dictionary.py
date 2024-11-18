from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db, get_current_user, User
from app.models.dictionary import DictionaryModel
from app.schemas.dictionary import Dictionary, DictionaryCreate, UpdateDictionary, DictionaryList

router = APIRouter(prefix="/api/dictionary")

# 辞書の登録処理
@router.post("/", response_model=Dictionary)
def create_dictionary_entry(dictionary: DictionaryCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_entry = DictionaryModel(term=dictionary.term, definition=dictionary.definition, user_id=current_user.user_id)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

# 特定の辞書の取得
@router.get("/{dictionary_id}", response_model=Dictionary)
def get_dictionary(dictionary_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    dictionary = db.query(DictionaryModel).filter(DictionaryModel.id == dictionary_id, DictionaryModel.user_id == current_user.user_id).first()
    if dictionary is None:
        raise HTTPException(status_code=404, detail="辞書のエントリーが見つかりません")
    return dictionary
        
# 全ての辞書の取得
@router.get("/", response_model=List[Dictionary])
def get_all_dictionaries(db: Session = Depends(get_db)):
    dictionaries = db.query(DictionaryModel).all()
    return dictionaries

# 特定の辞書の更新
@router.put("/{dictionary_id}", response_model=Dictionary)
def update_dictionary(dictionary_id: int, dictionary: UpdateDictionary, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    db_entry = db.query(DictionaryModel).filter(DictionaryModel.id == dictionary_id, DictionaryModel.user_id == current_user.user_id).first()
    if db_entry is None:
        raise HTTPException(status_code=404, detail="辞書のエントリーが見つかりません")
    if dictionary.term:
        db_entry.term = dictionary.term
    if dictionary.definition:
        db_entry.definition = dictionary.definition
    db.commit()
    db.refresh(db_entry)
    return db_entry
            
# 特定の辞書の削除    
@router.delete("/{dictionary_id}", response_model=dict)
def delete_dictionary(dictionary_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    db_entry = db.query(DictionaryModel).filter(DictionaryModel.id == dictionary_id, DictionaryModel.user_id == current_user.user_id).first()
    if db_entry is None:
        raise HTTPException(status_code=404, detail="削除対象のエントリーが見つかりません")
    db.delete(db_entry)
    db.commit()
    return {"message": "辞書を正常に削除しました"}
