import pprint
from typing import Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.account.schemas import Account
from app.address.models import Address
from app.address.schemas import AddressCreate, AddressUpdate
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


async def get(
    *,
    session: AsyncSession,
    address_id: int,
    parent: BaseModel,
) -> Optional[Store]:
    """Get a address by id and parent."""
    query = await session.execute(select(Address).filter_by(
        id=address_id, parent_id=parent.id,
        discriminator=parent.__class__.__name__.lower()
    ))
    address = query.scalar_one_or_none()
    await session.commit()

    return address


async def update(
    *, session: AsyncSession, address: Address, address_in: AddressUpdate
):
    """Update a address."""
    store_data = jsonable_encoder(address)
    update_data = address_in.dict(exclude_unset=True)

    for field in store_data:
        if field in update_data:
            setattr(address, field, update_data[field])

    await session.commit()

    return address


async def delete(*, session: AsyncSession, address: Address):
    """Delete a address."""
    await session.delete(address)
    await session.commit()
