from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "PapitoPet API"
    ADMIN_EMAIL: str = "fndmiranda@gmail.com"
    LOG_LEVEL: str = "INFO"
    SQLALCHEMY_WARN_20: int = 1
    ITEMS_PER_USER: int = 50
    SQLALCHEMY_DATABASE_URI: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ACCOUNT_EMAIL_VERIFY_ENABLE: bool = True
    ALGORITHM: str = "HS256"
    SECRET_KEY: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
