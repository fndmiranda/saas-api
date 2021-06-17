from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config import Settings
from app.user.models import User


async def authenticate_user(
    session: AsyncSession, username: str, password: str
):
    query = await session.execute(select(User).filter_by(email=username))
    user = query.scalar_one_or_none()
    await session.commit()

    if user is not None and user.check_password(password):
        return user

    return False


async def create_access_token(
    data: dict,
    settings: Settings,
    expires_delta: Optional[timedelta] = timedelta(minutes=15),
):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
