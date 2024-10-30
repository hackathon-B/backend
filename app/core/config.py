from pydantic import BaseSettings

class Settings(BaseSettings):
    # dbコンテナの環境変数
    DB_USER: str = "app_user"
    DB_PASSWORD: str = "app_password"
    DB_HOST: str = "db"  
    DB_PORT: str = "3306"
    DB_NAME: str = "app_db"

    # @propertyはメソッドを属性のようにアクセスできるデコレーター
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
