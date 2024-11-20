from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # dbコンテナの環境変数
    DB_USER: str = "app_user"
    DB_PASSWORD: str = "app_password"
    DB_HOST: str = "db"  
    DB_PORT: str = "3306"
    DB_NAME: str = "app_db"
    
    # openai_keyの設定
    OPENAI_API_KEY: str | None = None

    # Google認証関連の設定(OIDC)
    OIDC_ISSUER: str = "https://accounts.google.com"
    OIDC_CLIENT_ID: str | None = None
    OIDC_CLIENT_SECRET: str | None = None
    OIDC_REDIRECT_URI: str | None = None

    # JWTトークン関連の設定
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # @propertyはメソッドを属性のようにアクセスできるデコレーター
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # .envファイルから環境変数を読み込むように指定
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()