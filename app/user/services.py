from fastapi.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.account.schemas import AccountCreate
from app.user.models import User


class UserService:
    async def create(self, session: AsyncSession, account: AccountCreate):
        try:
            instance = User(**account.dict())
            session.add(instance)
            await session.commit()
            logger.info(
                "User created successfully with={}".format(
                    {
                        "user_id": instance.id,
                    }
                )
            )
            return instance
        except Exception as e:
            await session.rollback()
            logger.error(
                "Error in try create user with with={}".format(
                    {
                        "error": str(e),
                    }
                )
            )
            raise Exception(str(e))
