from datetime import datetime

from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.account.schemas import AccountCreate, AccountUpdate
from app.user.models import User


async def create(
    session: AsyncSession,
    account_in: AccountCreate,
    email_verified: bool = False,
):
    """Create a new user account."""
    create_data = account_in.dict()

    if email_verified:
        create_data.update({"email_verified_at": datetime.now()})

    instance = User(**create_data)
    session.add(instance)
    await session.commit()
    return instance


async def update(
    *, session: AsyncSession, account: User, account_in: AccountUpdate
):
    """Update a user account."""
    try:
        account_data = jsonable_encoder(account)
        update_data = account_in.dict(exclude_unset=True)

        for field in account_data:
            if field in update_data:
                setattr(account, field, update_data[field])

        session.add(account)
        await session.commit()

        logger.info(
            "User account updated successfully with={}".format(
                {
                    "user_id": account.id,
                }
            )
        )

        return account
    except Exception as e:
        logger.error(
            "Error in try update user account with with={}".format(
                {
                    "error": str(e),
                }
            )
        )
        raise Exception(str(e))


async def delete(*, session: AsyncSession, account: User):
    """Delete a user account."""
    try:
        await session.delete(account)
        await session.commit()

        logger.info(
            "User account deleted successfully with={}".format(
                {
                    "user_id": account.id,
                }
            )
        )
    except Exception as e:
        logger.error(
            "Error in try delete user account with with={}".format(
                {
                    "error": str(e),
                }
            )
        )
        raise Exception(str(e))
