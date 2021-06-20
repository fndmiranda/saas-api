import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.account import services
from app.account.schemas import Account, AccountCreate, AccountUpdate
from app.account.validators import validate_account
from app.depends import get_session
from app.oauth.depends import get_current_user_verified

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/accounts",
    summary="Create account.",
    response_model=Account,
    status_code=201,
)
async def create_account(
    *, session: AsyncSession = Depends(get_session), account_in: AccountCreate
):
    logger.info("Starting create user account")

    await validate_account(session=session, account_in=account_in)

    try:
        account = await services.create(session=session, account_in=account_in)
        logger.info(
            "User account created successfully with={}".format(
                {
                    "user_id": account.id,
                }
            )
        )
        return account
    except Exception as e:
        logger.error(
            "Error in try create user account with with={}".format(
                {
                    "error": str(e),
                }
            )
        )
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/accounts",
    summary="Get account.",
    response_model=Account,
)
async def get_account(
    *, account_in: Account = Depends(get_current_user_verified)
):
    logger.info(
        "Response of get user account with={}".format(
            {"user_id": account_in.id}
        )
    )
    return account_in


@router.put(
    "/accounts",
    summary="Update account.",
    response_model=Account,
)
async def update_account(
    *,
    session: AsyncSession = Depends(get_session),
    account: Account = Depends(get_current_user_verified),
    account_in: AccountUpdate
):
    await validate_account(
        session=session, account_in=account_in, account=account
    )

    await services.update(
        session=session, account=account, account_in=account_in
    )

    logger.info(
        "Response of update user account with={}".format(
            {"user_id": account.id}
        )
    )

    return account


@router.delete(
    "/accounts",
    summary="Delete account.",
    status_code=204,
)
async def delete_account(
    *,
    session: AsyncSession = Depends(get_session),
    account: Account = Depends(get_current_user_verified)
):
    await services.delete(session=session, account=account)

    return JSONResponse(status_code=204)
