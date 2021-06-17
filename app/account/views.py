import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.account.schemas import Account, AccountCreate
from app.dependencies import get_session
from app.user.services import UserService

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

    return await UserService().create(session=session, account=account)
