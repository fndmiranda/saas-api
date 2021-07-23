import logging
import pprint

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.account.schemas import Account
from app.auth.depends import (
    current_user_verified,
    current_user_admin,
)
from app.core.depends import common_parameters
from app.address.schemas import AddressCreate, Address, AddressPagination, \
    AddressUpdate
from app.core.services import search_filter_sort_paginate
from app.depends import get_session
from app.store.models import Store as StoreModel
from app.address.models import Address as AddressModel
from app.store.schemas import Store, StoreCreate, StoreUpdate
from app.address.services import create, get, update, delete
from app.store.services.store import get as get_store
from app.store.validators import validate_store, validate_store_owner_or_admin

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/stores/{store_id}/addresses",
    summary="Create store address.",
    response_model=Address,
    status_code=status.HTTP_201_CREATED,
)
async def create_store_address(
    *, session: AsyncSession = Depends(get_session), address_in: AddressCreate,
    account: Account = Depends(current_user_verified), store_id: int,
):
    store = await get_store(session=session, store_id=store_id)

    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found."
        )

    await validate_store_owner_or_admin(
        session=session, store=store, account=account
    )

    logger.info(
        "Starting create store address with={}".format(
            {
                "address_in": address_in,
                "owner_in": account.id,
            }
        )
    )

    address = await create(
        session=session, parent=store, address_in=address_in
    )

    logger.info(
        "Store address created successfully with={}".format(
            {
                "store_id": store_id,
                "address_id": address.id,
            }
        )
    )
    return address


@router.get(
    "/stores/{store_id}/addresses",
    summary="Get store addresses.",
    response_model=AddressPagination,
)
async def get_store_addresses(
    *,
    session: AsyncSession = Depends(get_session),
    common: dict = Depends(common_parameters), store_id: int
):
    common["filter_spec"].append({
        "model": "Address",
        "field": "parent_id",
        "op": "eq",
        "value": store_id
    })

    logger.info(f"Starting get store addresses with={common}")

    pagination = await search_filter_sort_paginate(
        session=session, model=AddressModel, **common
    )

    logger.info(
        "Store addresses got successfully with={}".format(
            {
                "page": pagination["page"],
                "items": len(pagination["items"]),
                "per_page": pagination["per_page"],
                "parameters": common,
                "num_pages": pagination["num_pages"],
                "total": pagination["total"],
            }
        )
    )

    return pagination


@router.get(
    "/stores/{store_id}/addresses/{address_id}",
    summary="Get store address.",
    dependencies=[Depends(current_user_verified)],
    response_model=Address,
)
async def get_store_address(
    *, session: AsyncSession = Depends(get_session),
    store_id: int, address_id: int
):
    logger.info(
        "Starting get store address with={}".format(
            {
                "address_id": address_id,
                "store_id": store_id,
            }
        )
    )

    store = await get_store(session=session, store_id=store_id)

    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found."
        )

    address = await get(session=session, address_id=address_id, parent=store)

    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found."
        )

    logger.info(
        "Store address got successfully with={}".format(
            {
                "address_id": address.id,
                "postcode": address.postcode,
            }
        )
    )

    return address


@router.put(
    "/stores/{store_id}/addresses/{address_id}",
    summary="Update store address.",
    response_model=Address,
)
async def update_store_address(
    *,
    session: AsyncSession = Depends(get_session),
    store_id: int,
    address_id: int,
    address_in: AddressUpdate,
    account: Account = Depends(current_user_verified),
):
    logger.info(
        "Starting update store address with={}".format(
            {
                "store_id": store_id,
                "address_id": address_id,
                "address_in": address_in,
            }
        )
    )

    store = await get_store(session=session, store_id=store_id)
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found."
        )

    await validate_store_owner_or_admin(
        session=session, store=store, account=account
    )

    address = await get(session=session, address_id=address_id, parent=store)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found."
        )

    address = await update(
        session=session, address_in=address_in, address=address
    )
    logger.info(
        "Store address updated successfully with={}".format(
            {
                "address": address.dict(),
            }
        )
    )
    return address


@router.delete(
    "/stores/{store_id}/addresses/{address_id}",
    summary="Delete store address.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_store_address(
    *,
    session: AsyncSession = Depends(get_session),
    store_id: int,
    address_id: int,
    account: Account = Depends(current_user_verified),
):
    logger.info(
        "Starting delete store address with={}".format({
            "address_id": address_id,
            "store_id": store_id,
        })
    )

    store = await get_store(session=session, store_id=store_id)
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found."
        )

    await validate_store_owner_or_admin(
        session=session, store=store, account=account
    )

    address = await get(session=session, address_id=address_id, parent=store)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found."
        )

    await delete(session=session, address=address)

    logger.info(
        "Store address deleted successfully with={}".format(
            {
                "address_id": address_id,
                "store_id": store_id,
            }
        )
    )

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
