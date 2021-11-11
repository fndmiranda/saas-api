from datetime import datetime, timedelta

from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config import get_settings
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


async def create_access_token(user: User):
    settings = get_settings()
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"sub": user.email}
    expire = datetime.utcnow() + access_token_expires
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return {"access_token": encoded_jwt, "token_type": "bearer"}
