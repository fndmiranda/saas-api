from sqlalchemy.ext.asyncio import AsyncSession

from app.account.schemas import AccountCreate
from app.user.models import User


class UserService:
    async def create(self, session: AsyncSession, account: AccountCreate):
        try:
            instance = User(**account.dict())
            session.add(instance)
            await session.commit()
            return instance
        except Exception as e:
            await session.rollback()
            raise Exception(str(e))
