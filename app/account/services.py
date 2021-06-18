from datetime import datetime

from fastapi.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.account.schemas import AccountCreate
from app.config import get_settings
from app.user.models import User


async def create(session: AsyncSession, account: AccountCreate, email_verified: bool = False):
    try:
        settings = get_settings()
        data = account.dict()

        if not settings.ACCOUNT_EMAIL_VERIFY_ENABLE or email_verified:
            data.update({"email_verified_at": datetime.now()})

        instance = User(**data)
        session.add(instance)
        await session.commit()
        logger.info(
            "User account created successfully with={}".format(
                {
                    "user_id": instance.id,
                }
            )
        )
        return instance
    except Exception as e:
        await session.rollback()
        logger.error(
            "Error in try create user account with with={}".format(
                {
                    "error": str(e),
                }
            )
        )
        raise Exception(str(e))
