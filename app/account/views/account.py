import logging

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.account.schemas import Account, AccountCreate, AccountUpdate
from app.account.services.account import create, delete, update
from app.account.services.verified import generate_verify_email_url
from app.account.validators import validate_account
from app.auth.depends import current_user_verified
from app.config import get_settings
from app.depends import get_session
from app.notification.tasks import send_mail_verification

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/accounts",
    summary="Create account.",
    response_model=Account,
    status_code=status.HTTP_201_CREATED,
)
async def create_account(
    *,
    session: AsyncSession = Depends(get_session),
    account_in: AccountCreate,
    request: Request
):
    logger.info("Starting create user account")
    settings = get_settings()

    await validate_account(session=session, account_in=account_in)

    account = await create(session=session, account_in=account_in)
    logger.info(
        "User account created successfully with={}".format(
            {
                "user_id": account.id,
            }
        )
    )

    if settings.ACCOUNT_EMAIL_VERIFY_ENABLE:
        url = await generate_verify_email_url(account=account, request=request)
        task_id = send_mail_verification.delay(
            account_id=account.id,
            url=url,
        )
        logger.info(
            "Create task to send email verification with={}".format(
                {
                    "user_id": account.id,
                    "task_id": task_id,
                }
            )
        )

    return account


@router.get(
    "/accounts",
    summary="Get account.",
    response_model=Account,
)
async def get_account(*, account_in: Account = Depends(current_user_verified)):
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
    account: Account = Depends(current_user_verified),
    account_in: AccountUpdate
):
    await validate_account(
        session=session, account_in=account_in, account=account
    )

    await update(session=session, account=account, account_in=account_in)

    logger.info(
        "Response of update user account with={}".format(
            {"user_id": account.id}
        )
    )

    return account


@router.delete(
    "/accounts",
    summary="Delete account.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_account(
    *,
    session: AsyncSession = Depends(get_session),
    account: Account = Depends(current_user_verified)
):
    await delete(session=session, account=account)

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
