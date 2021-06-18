import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.account import services
from app.account.schemas import Account, AccountCreate
from app.dependencies import get_session
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
    *, session: AsyncSession = Depends(get_session), account: AccountCreate
):
    logger.info("Starting create user account")

    response = await services.create(session=session, account=account)

    logger.info(
        "Response of create user account with={}".format(
            {"user_id": response.id}
        )
    )

    return response


@router.get(
    "/accounts",
    summary="Get account.",
    response_model=Account,
)
async def get_account(*, current_user: Account = Depends(get_current_user_verified)):
    logger.info(
        "Response of get user account with={}".format(
            {"user_id": current_user.id}
        )
    )
    return current_user
