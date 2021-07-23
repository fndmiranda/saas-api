import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.account.schemas import Account
from app.address.models import Address as AddressModel
from app.address.schemas import (
    Address,
    AddressCreate,
    AddressPagination,
    AddressUpdate,
)
from app.address.services import create, delete, get, update
from app.auth.depends import current_user_verified
from app.core.depends import common_parameters
from app.core.services import search_filter_sort_paginate
from app.depends import get_session

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/accounts/addresses",
    summary="Create account address.",
    response_model=Address,
    status_code=status.HTTP_201_CREATED,
)
async def create_account_address(
    *,
    session: AsyncSession = Depends(get_session),
    address_in: AddressCreate,
    account: Account = Depends(current_user_verified),
):
    logger.info(
        "Starting create account address with={}".format(
            {
                "address_in": address_in,
                "user_id": account.id,
            }
        )
    )

    address = await create(
        session=session, parent=account, address_in=address_in
    )

    logger.info(
        "Account address created successfully with={}".format(
            {
                "user_id": account.id,
                "address_id": address.id,
            }
        )
    )
    return address


@router.get(
    "/accounts/addresses",
    summary="Get account addresses.",
    response_model=AddressPagination,
)
async def get_account_addresses(
    *,
    session: AsyncSession = Depends(get_session),
    common: dict = Depends(common_parameters),
    account: Account = Depends(current_user_verified),
):
    common["filter_spec"].append(
        {
            "model": "Address",
            "field": "parent_id",
            "op": "eq",
            "value": account.id,
        }
    )

    logger.info(f"Starting get account addresses with={common}")

    pagination = await search_filter_sort_paginate(
        session=session, model=AddressModel, **common
    )

    logger.info(
        "Account addresses got successfully with={}".format(
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
    "/accounts/addresses/{address_id}",
    summary="Get account address.",
    response_model=Address,
)
async def get_account_address(
    *,
    session: AsyncSession = Depends(get_session),
    address_id: int,
    account: Account = Depends(current_user_verified),
):
    logger.info(
        "Starting get account address with={}".format(
            {
                "address_id": address_id,
                "user_id": account.id,
            }
        )
    )

    address = await get(session=session, address_id=address_id, parent=account)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found."
        )

    logger.info(
        "Account address got successfully with={}".format(
            {
                "address_id": address.id,
                "postcode": address.postcode,
            }
        )
    )

    return address


@router.put(
    "/accounts/addresses/{address_id}",
    summary="Update account address.",
    response_model=Address,
)
async def update_account_address(
    *,
    session: AsyncSession = Depends(get_session),
    address_id: int,
    address_in: AddressUpdate,
    account: Account = Depends(current_user_verified),
):
    logger.info(
        "Starting update account address with={}".format(
            {
                "user_id": account.id,
                "address_id": address_id,
                "address_in": address_in,
            }
        )
    )

    address = await get(session=session, address_id=address_id, parent=account)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found."
        )

    address = await update(
        session=session, address_in=address_in, address=address
    )
    logger.info(
        "Account address updated successfully with={}".format(
            {
                "address": address.dict(),
            }
        )
    )
    return address


@router.delete(
    "/accounts/addresses/{address_id}",
    summary="Delete account address.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_account_address(
    *,
    session: AsyncSession = Depends(get_session),
    address_id: int,
    account: Account = Depends(current_user_verified),
):
    logger.info(
        "Starting delete account address with={}".format(
            {
                "address_id": address_id,
                "user_id": account.id,
            }
        )
    )

    address = await get(session=session, address_id=address_id, parent=account)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found."
        )

    await delete(session=session, address=address)

    logger.info(
        "Account address deleted successfully with={}".format(
            {
                "address_id": address_id,
                "user_id": account.id,
            }
        )
    )

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
