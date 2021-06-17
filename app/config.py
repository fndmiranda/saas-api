from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "PapitoPet API"
    ADMIN_EMAIL: str = "fndmiranda@gmail.com"
    SQLALCHEMY_WARN_20: int = 1
    ITEMS_PER_USER: int = 50
    SQLALCHEMY_DATABASE_URI: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    SECRET_KEY: str

    class Config:
        env_file = ".env"
