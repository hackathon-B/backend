from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db, get_current_user
from app.models.dictionary import Dictionary
from app.schemas.dictionary import DictionaryCreate, DictionaryUpdate, DictionaryEntry, DictionaryListResponse
from app.schemas.dictionary import DeleteResponse
from app.models.user import User

router = APIRouter(prefix="/api/dictionary")

# 辞書の登録処理
@router.post("", response_model=DictionaryEntry)
def create_dictionary_entry(
    dictionary: DictionaryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 空のタイトル又は内容が登録されないようにするチェック
    if not dictionary.term.strip(): 
        raise HTTPException(status_code=400, detail="タイトルが空です。入力してください。")
    if not dictionary.definition.strip():
        raise HTTPException(status_code=400, detail="内容が空です。入力してください。")
    
    # 既存のエントリーのチェック
    existing_entry = db.query(Dictionary).filter(
        Dictionary.term == dictionary.term,
        Dictionary.user_id == current_user.user_id
    ).first()
    if existing_entry:
        raise HTTPException(status_code=400, detail="このタイトルは既に登録されています。")
    
    # 新しい辞書の登録
    db_entry = Dictionary(
        term=dictionary.term,
        definition=dictionary.definition,
        user_id=current_user.user_id
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry
    
# 全ての辞書の取得
@router.get("", response_model=DictionaryListResponse)
def get_all_dictionaries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dictionaries = db.query(Dictionary).filter(
        Dictionary.user_id == current_user.user_id
    ).all()
    return {"dictionaries": dictionaries}

# 特定の辞書の取得
@router.get("/{dictionary_id}", response_model=DictionaryEntry)
def get_dictionary(
    dictionary_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dictionary = db.query(Dictionary).filter(
        Dictionary.id == dictionary_id,
        Dictionary.user_id == current_user.user_id
    ).first()
    if not dictionary:
        raise HTTPException(status_code=404, detail="辞書のエントリーが見つかりません。")
    return dictionary

# 特定の辞書の更新
@router.put("/{dictionary_id}", response_model=DictionaryEntry)
def update_dictionary(
    dictionary_id: int,
    dictionary: DictionaryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_entry = db.query(Dictionary).filter(
        Dictionary.id== dictionary_id,
        Dictionary.user_id == current_user.user_id
    ).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="辞書のエントリーが見つかりません。")
    # 空チェックを実施
    if dictionary.term is not None and not dictionary.term.strip():
        raise HTTPException(status_code=400, detail="タイトルが空です。入力してください。")
    if dictionary.definition is not None and not dictionary.definition.strip():
        raise HTTPException(status_code=400, detail="内容が空です。入力してください。")
    # 更新処理
    if dictionary.term:
        db_entry.term = dictionary.term
    if dictionary.definition:
        db_entry.definition = dictionary.definition
    
    db.commit()
    db.refresh(db_entry)
    return db_entry

# 特定の辞書の削除
@router.delete("/{dictionary_id}", response_model=DeleteResponse)
def delete_dictionary(
    dictionary_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_entry = db.query(Dictionary).filter(
        Dictionary.id == dictionary_id,
        Dictionary.user_id == current_user.user_id
    ).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="削除対象のエントリーが見つかりません。")
    db.delete(db_entry)
    db.commit()
    return {"message": "辞書を正常に削除しました。"}
