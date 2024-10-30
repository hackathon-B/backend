from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        # クラス名を自動で小文字にしてテーブル名にする
        return cls.__name__.lower()