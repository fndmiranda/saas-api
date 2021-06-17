import logging
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.dependencies import get_session, get_settings
from app.oauth import services
from app.oauth.schemas import Token

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/token", response_model=Token)
async def create_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
    settings: Settings = Depends(get_settings),
):
    user = await services.authenticate_user(
        session, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = await services.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
        settings=settings,
    )
    return {"access_token": access_token, "token_type": "bearer"}
