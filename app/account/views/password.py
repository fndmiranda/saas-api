import logging
import pprint
from datetime import datetime, timedelta
from secrets import token_urlsafe

from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.account.depends import password_reset_form_parameters
from app.account.schemas import Account, AccountCreate, AccountUpdate, \
    PasswordResetTokenCreate, PasswordResetToken, PasswordResetCreate
from app.account.services.account import get_by_email
from app.account.services.password import generate_password_reset_url, create_reset
from app.account.validators import validate_account
from app.auth.depends import current_user_verified
from app.config import get_settings
from app.depends import get_session
from app.account.tasks import send_mail_reset_password

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/accounts/password-reset-token",
    summary="Send a password reset link with token to the given account.",
    status_code=status.HTTP_202_ACCEPTED,
)
async def create_password_reset_token(
    *, session: AsyncSession = Depends(get_session),
    request: Request,
    reset_in: PasswordResetTokenCreate
):
    logger.info("Starting create password reset token")

    settings = get_settings()

    account = await get_by_email(session=session, email=reset_in.email)

    if account:
        url, token = await generate_password_reset_url(
            account=account, request=request
        )

        expire_at = datetime.now() + timedelta(
            minutes=settings.PASSWORD_RESET_EXPIRE_MINUTES
        )

        reset_in = PasswordResetCreate(**{
            "email": account.email,
            "token": token,
            "expire_at": expire_at,
        })

        instance = await create_reset(session=session, reset_in=reset_in)

        task_id = send_mail_reset_password.delay(
            account_id=account.id, name=account.name,
            email=account.email, url=url,
        )

        logger.info(
            "Password reset token created successfully with={}".format(
                {
                    "user_id": account.id,
                    "reset_id": instance.id,
                    "task_id": task_id,
                    "expire_at": expire_at,
                }
            )
        )

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED)


@router.get(
    "/accounts/password-reset-form",
    summary="Form to reset password to the given token.",
)
async def password_reset_form(
    *, session: AsyncSession = Depends(get_session),
    params: dict = Depends(password_reset_form_parameters),
):
    logger.info("Starting password reset")

    # account = await get_by_email(session=session, email=reset_in.email)
    #
    # if account:
    #     services.send_password_reset_token(account=account)
    #
    #     logger.info(
    #         "Password reset token created successfully with={}".format(
    #             {
    #                 "user_id": account.id,
    #             }
    #         )
    #     )

    return JSONResponse(status_code=status.HTTP_200_OK)


# @router.get(
#     "/accounts",
#     summary="Get account.",
#     response_model=Account,
# )
# async def get_account(*, account_in: Account = Depends(current_user_verified)):
#     logger.info(
#         "Response of get user account with={}".format(
#             {"user_id": account_in.id}
#         )
#     )
#     return account_in
#
#
# @router.put(
#     "/accounts",
#     summary="Update account.",
#     response_model=Account,
# )
# async def update_account(
#     *,
#     session: AsyncSession = Depends(get_session),
#     account: Account = Depends(current_user_verified),
#     account_in: AccountUpdate
# ):
#     await validate_account(
#         session=session, account_in=account_in, account=account
#     )
#
#     await services.update(
#         session=session, account=account, account_in=account_in
#     )
#
#     logger.info(
#         "Response of update user account with={}".format(
#             {"user_id": account.id}
#         )
#     )
#
#     return account
#
#
# @router.delete(
#     "/accounts",
#     summary="Delete account.",
#     status_code=204,
# )
# async def delete_account(
#     *,
#     session: AsyncSession = Depends(get_session),
#     account: Account = Depends(current_user_verified)
# ):
#     await services.delete(session=session, account=account)
#
#     return JSONResponse(status_code=204)
