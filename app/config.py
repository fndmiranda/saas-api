from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_TITLE = "SaaS Api"
    APP_NAME: str = "saas-api"
    ADMIN_EMAIL: str = "fndmiranda@gmail.com"
    LOG_LEVEL: str = "INFO"
    DEFAULT_ITEMS_PER_PAGE: int = 5
    MAX_ITEMS_PER_PAGE: int = 25
    SQLALCHEMY_WARN_20: int = 1
    ITEMS_PER_USER: int = 50
    SQLALCHEMY_DATABASE_URI: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ACCOUNT_EMAIL_VERIFY_ENABLE: bool = True
    TESTING: bool = False
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = (
        "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )
    CSRF_SECRET: str = "c852338422c9f6b8847cb736eab00a72b3168f9e"

    PASSWORD_RESET_EXPIRE_MINUTES: int = 60
    MAIL_DEFAULT_FROM_NAME: str = "SaaS Api"
    MAIL_DEFAULT_FROM_EMAIL: str = "no-reply@yourdomain.com"
    SENDGRID_API_URL: str = "https://api.sendgrid.com/v3/mail/send"
    SENDGRID_API_KEY: str = "YourSendgridApiKey"

    CELERY_BROKER_URL: str = "sqla+sqlite:///instance/database.db"
    CELERY_RESULT_BACKEND: str = "db+sqlite:///instance/database.db"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
