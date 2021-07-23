from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.account.schemas import AccountCreate, AccountUpdate
from app.address.models import Address
from app.user.models import User


async def create(
    session: AsyncSession,
    account_in: AccountCreate,
    email_verified: bool = False,
):
    """Create a new user account."""
    create_data = account_in.dict()

    if create_data.get("addresses"):
        create_data.update(
            {
                "addresses": [
                    Address(**address)
                    for address in create_data.get("addresses")
                ]
            }
        )
    else:
        create_data.pop("addresses")

    if email_verified:
        create_data.update({"email_verified_at": datetime.now()})

    instance = User(**create_data)
    session.add(instance)
    await session.commit()
    return instance


async def get(
    *,
    session: AsyncSession,
    account_id: int,
) -> Optional[User]:
    """Get a account by id."""
    query = await session.execute(select(User).filter_by(id=account_id))
    account = query.scalar_one_or_none()
    await session.commit()

    return account


async def update(
    *, session: AsyncSession, account: User, account_in: AccountUpdate
):
    """Update a account."""
    account_data = jsonable_encoder(account)
    update_data = account_in.dict(exclude_unset=True)

    for field in account_data:
        if field in update_data:
            setattr(account, field, update_data[field])

    session.add(account)
    await session.commit()

    logger.info(
        "Account updated successfully with={}".format(
            {
                "user_id": account.id,
            }
        )
    )

    return account


async def delete(*, session: AsyncSession, account: User):
    """Delete a account."""
    await session.delete(account)
    await session.commit()

    logger.info(
        "Account deleted successfully with={}".format(
            {
                "user_id": account.id,
            }
        )
    )
