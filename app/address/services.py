import pprint
from typing import Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.account.schemas import Account
from app.address.models import Address
from app.address.schemas import AddressCreate
from app.store.models import Store, StorePerson
from app.store.schemas import StoreCreate, StoreUpdate


async def create(
    *,
    session: AsyncSession,
    address_in: AddressCreate,
    parent: BaseModel,
):
    """Create a new address."""
    create_data = address_in.dict()
    create_data.update({
        "parent_id": parent.id,
        "discriminator": parent.__class__.__name__.lower(),
    })

    address = Address(**create_data)
    session.add(address)

    await session.commit()
    return address
#
#
# async def get(
#     *,
#     session: AsyncSession,
#     store_id: int,
# ) -> Optional[Store]:
#     """Get a store by id."""
#     query = await session.execute(select(Store).filter_by(id=store_id))
#     store = query.scalar_one_or_none()
#     await session.commit()
#
#     return store
#
#
# async def update(
#     *, session: AsyncSession, store: Store, store_in: StoreUpdate
# ):
#     """Update a store."""
#     store_data = jsonable_encoder(store)
#     update_data = store_in.dict(exclude_unset=True)
#
#     for field in store_data:
#         if field in update_data:
#             setattr(store, field, update_data[field])
#
#     await session.commit()
#
#     return store
#
#
# async def delete(*, session: AsyncSession, store: Store):
#     """Delete a store."""
#     await session.delete(store)
#     await session.commit()
