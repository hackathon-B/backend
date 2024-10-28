# backend
バックエンド用のリポジトリ

<pre>
.
app
├── api
│   ├── endpoints       # routerとパスオペレーション関数
│   ├── deps.py         # Depends()に含める関数
│   └── api.py          # endpointsのrouterをひとつにまとめる
├── core
│   ├── config.py       # 設定値
│   └── security.py     # パスワードのハッシュ化やJWTの発行
├── crud                # DBのCRUD操作
├── db
│   ├── base.py         # マイグレーション用にBaseとmodelsを全て読み込む
│   ├── base_class.py   # SQLAlchemyのBaseクラスを定義
│   └── session.py      # DBのsessionmakerを記述
├── schemas             # pydanticを使ってリクエストボディやレスポンスボディの型を定義
├── models              # SQLAlchemyのモデルを定義
└── main.py             # api/api.pyのrouterをapp=FastAPI()に加える
</pre>