import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.account.schemas import Account, AccountEmailVerify
from app.account.services.account import get
from app.account.services.verified import (
    generate_verify_email_url,
    mark_email_as_verified,
    signature_is_valid,
)
from app.account.tasks import send_mail_verification
from app.auth.depends import current_user
from app.config import get_settings
from app.depends import get_session

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/accounts/email-verified",
    summary="Check if account has verified their email address.",
)
async def email_verified(*, account_in: Account = Depends(current_user)):
    logger.info(
        "Starting check if account has verified their email with={}".format(
            {"user_id": account_in.id}
        )
    )

    if account_in.email_verified_at is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not verified",
        )

    return JSONResponse(status_code=status.HTTP_200_OK)


@router.get(
    "/accounts/email-verified-resend",
    summary="Resend account verify email.",
    status_code=status.HTTP_201_CREATED,
)
async def resend_email_verified(
    *, account_in: Account = Depends(current_user), request: Request
):
    logger.info(
        "Starting resend email verified account with={}".format(
            {"user_id": account_in.id}
        )
    )

    if account_in.email_verified_at is not None:
        logger.info(
            "Account email already verified with={}".format(
                {"user_id": account_in.id}
            )
        )
        return JSONResponse(status_code=status.HTTP_200_OK)

    url = await generate_verify_email_url(account=account_in, request=request)
    task_id = send_mail_verification.delay(
        account_id=account_in.id,
        name=account_in.name,
        email=account_in.email,
        url=url,
    )
    logger.info(
        "Task to resend email verified created successfully with={}".format(
            {"user_id": account_in.id, "task_id": task_id}
        )
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED)


@router.get(
    "/accounts/email-verify/{user_id}/{signature}",
    summary="Email account verify.",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def email_verify(
    *,
    session: AsyncSession = Depends(get_session),
    request: Request,
    user_id: int,
    signature: str
):
    from app.main import templates

    logger.info(
        "Starting email account verify with={}".format({"user_id": user_id})
    )

    settings = get_settings()

    account = await get(session=session, account_id=user_id)

    if account:
        is_valid = await signature_is_valid(
            account=account,
            signature=signature,
        )

        if is_valid:
            verify_in = AccountEmailVerify(
                **{"email_verified_at": datetime.now()}
            )
            if account.email_verified_at is None:
                await mark_email_as_verified(
                    session=session,
                    account=account,
                    verify_in=verify_in,
                )
                logger.info(
                    "Email account verify with success with={}".format(
                        {"user_id": user_id}
                    )
                )

            return templates.TemplateResponse(
                "show_message.html",
                {
                    "request": request,
                    "datetime": datetime,
                    "color": "green",
                    "message": "Email account verify with success!",
                    "app_title": settings.APP_TITLE,
                },
            )

    logger.error(
        "Error in email account verify with={}".format({"user_id": user_id})
    )
    return templates.TemplateResponse(
        "show_message.html",
        {
            "request": request,
            "datetime": datetime,
            "color": "red",
            "message": "Error in email account verify!",
            "app_title": settings.APP_TITLE,
        },
    )
