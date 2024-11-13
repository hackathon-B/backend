from typing import List, Optional, Generic, TypeVar, Type

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from app.db.base_class import Base

# 型変数の定義
ModelType = TypeVar("ModelType", bound=Base)  # SQLAlchemyのBaseクラスを継承するモデルクラス
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)  # PydanticのBaseModelを継承する作成用スキーマ
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)  # PydanticのBaseModelを継承する更新用スキーマ

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUDオブジェクトの初期化メソッド。
        **パラメータ**
            `model`: SQLAlchemyモデルクラス（データベースのテーブルに対応）
        """
        self.model = model
        
    def get(self, db_session: Session, id: int) -> Optional[ModelType]:
        # 指定されたIDを持つレコードを取得
        primary_key_column = inspect(self.model).primary_key[0]
        obj = db_session.query(self.model).filter(primary_key_column == id).first()
        if obj is None:
            raise ValueError(f"Record with id {id} not found.")
        return obj
        
    
    def get_multi(self, db_session: Session, *, skip=0, limit=100) -> List[ModelType]:
        # 複数のレコードを取得。*の後はキーワードで引数を使用する必要がある
        return db_session.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, db_session: Session, *, obj_in: CreateSchemaType) -> ModelType:
        # 新しいレコードを作成
        # `obj_in`をJSON形式にエンコードしてからモデルに渡し、データベースに保存する
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # SQLAlchemyモデルのインスタンスを作成
        db_session.add(db_obj)  # 新しいオブジェクトをセッションに追加
        try:
            db_session.commit()  # トランザクションをコミットし、データベースに保存
        except Exception as e:
            db_session.rollback()  # エラーが発生した場合はロールバック
            raise e
        db_session.refresh(db_obj)  # 最新の状態にリフレッシュ
        return db_obj
    
    def update(
        self, db_session: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        # 既存のレコードを更新する
        # `obj_in`に含まれるフィールドのみ更新する
        obj_data = jsonable_encoder(db_obj)  # 既存のデータをJSON形式に変換
        update_data = obj_in.dict(exclude_unset=True)  # 未設定のフィールドを除外して辞書化
        for field in obj_data:
            if field in update_data:  # 更新データにフィールドが含まれていれば、その値を設定
                setattr(db_obj, field, update_data[field])
        db_session.add(db_obj)  # 更新したオブジェクトをセッションに追加
        try:
            db_session.commit()  # トランザクションをコミットし、データベースに保存
        except Exception as e:
            db_session.rollback()  # エラーが発生した場合はロールバック
            raise e 
        db_session.refresh(db_obj)  # 最新の状態にリフレッシュ
        return db_obj
    
    def remove(self, db_session: Session, *, id: int) -> ModelType:
        # 指定されたIDレコードを削除する
        primary_key_column = inspect(self.model).primary_key[0]
        obj = db_session.query(self.model).filter(primary_key_column == id).first()  # 削除対象のオブジェクトを取得
        if obj in None:
            raise ValueError(f"Record with id {id} not found.")
        db_session.delete(obj)  # オブジェクトをセッションから削除
        try:           
            db_session.commit()  # トランザクションをコミットし、データベースから削除
        except Exception as e:
            db_session.rollback()  # エラーが発生した場合はロールバック
            raise e 
        return obj

