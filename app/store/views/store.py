import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.account.schemas import Account
from app.auth.depends import current_user_verified
from app.core.depends import common_parameters
from app.core.services import search_filter_sort_paginate
from app.depends import get_session
from app.store.models import Store as StoreModel
from app.store.schemas import Store, StoreCreate, StorePagination, StoreUpdate
from app.store.services.store import create, delete, get, update
from app.store.validators import validate_store, validate_store_owner_or_admin

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/stores",
    summary="Create store.",
    response_model=Store,
    status_code=status.HTTP_201_CREATED,
)
async def create_store(
    *,
    session: AsyncSession = Depends(get_session),
    store_in: StoreCreate,
    account: Account = Depends(current_user_verified),
):
    logger.info(
        "Starting create store with={}".format(
            {
                "store_in": store_in,
                "owner_in": account.id,
            }
        )
    )

    await validate_store(session=session, store_in=store_in)

    store = await create(session=session, store_in=store_in, owner=account)
    logger.info(
        "Store created successfully with={}".format(
            {
                "store": store,
                "owner_id": account.id,
            }
        )
    )
    return store


@router.get(
    "/stores",
    summary="Get stores.",
    response_model=StorePagination,
)
async def get_stores(
    *,
    session: AsyncSession = Depends(get_session),
    common: dict = Depends(common_parameters),
):
    logger.info(f"Starting get stores with={common}")

    pagination = await search_filter_sort_paginate(
        session=session, model=StoreModel, **common
    )

    logger.info(
        "Stores got successfully with={}".format(
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
    "/stores/{store_id}",
    summary="Get store.",
    dependencies=[Depends(current_user_verified)],
    response_model=Store,
)
async def get_store(
    *, session: AsyncSession = Depends(get_session), store_id: int
):
    logger.info(
        "Starting get store with={}".format(
            {
                "store_id": store_id,
            }
        )
    )

    store = await get(session=session, store_id=store_id)
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found."
        )

    logger.info(
        "Store got successfully with={}".format(
            {
                "store": store,
            }
        )
    )

    return store


@router.put(
    "/stores/{store_id}",
    summary="Update store.",
    response_model=Store,
)
async def update_store(
    *,
    session: AsyncSession = Depends(get_session),
    store_id: int,
    store_in: StoreUpdate,
    account: Account = Depends(current_user_verified),
):
    logger.info(
        "Starting update store with={}".format(
            {
                "store_id": store_id,
                "store_in": store_in,
            }
        )
    )

    store = await get(session=session, store_id=store_id)

    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found."
        )

    await validate_store_owner_or_admin(
        session=session, store=store, account=account
    )

    await validate_store(session=session, store_in=store_in, store=store)

    store = await update(session=session, store_in=store_in, store=store)
    logger.info(
        "Store updated successfully with={}".format(
            {
                "store": store.dict(),
            }
        )
    )
    return store


@router.delete(
    "/stores/{store_id}",
    summary="Delete store.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_store(
    *,
    session: AsyncSession = Depends(get_session),
    store_id: int,
    account: Account = Depends(current_user_verified),
):
    logger.info("Starting delete store with={}".format({"store_id": store_id}))

    store = await get(session=session, store_id=store_id)

    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found."
        )

    await validate_store_owner_or_admin(
        session=session, store=store, account=account
    )

    await delete(session=session, store=store)

    logger.info(
        "Store deleted successfully with={}".format(
            {
                "store_id": store_id,
            }
        )
    )

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
