from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config import get_settings
from app.depends import get_session
from app.user.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
):
    settings = get_settings()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    query = await session.execute(select(User).filter_by(email=username))
    user = query.scalar_one_or_none()
    await session.commit()

    if user is None:
        raise credentials_exception
    return user


async def get_current_user_verified(
    current_user: User = Depends(get_current_user),
):
    settings = get_settings()

    if (
        settings.ACCOUNT_EMAIL_VERIFY_ENABLE
        and current_user.email_verified_at is None
    ):
        raise HTTPException(status_code=403, detail="Email not verified")
    return current_user
