from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.database import async_session


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@lru_cache()
def get_settings() -> Settings:
    return Settings()
