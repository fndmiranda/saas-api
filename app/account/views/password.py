import logging
from datetime import datetime

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette_wtf import csrf_protect

from app.account.forms import PasswordResetForm
from app.account.schemas import AccountUpdate, PasswordResetTokenCreate
from app.account.services.account import get_by_email, update
from app.account.services.password import (
    create_reset,
    generate_password_reset_url,
    is_valid_token,
)
from app.account.tasks import send_mail_reset_password
from app.config import get_settings
from app.depends import get_session

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/accounts/password-reset-token",
    summary="Send a password reset link with token to the given account.",
    status_code=status.HTTP_202_ACCEPTED,
)
async def create_password_reset_token(
    *,
    session: AsyncSession = Depends(get_session),
    request: Request,
    reset_in: PasswordResetTokenCreate,
):
    logger.info("Starting create password reset token")

    account = await get_by_email(session=session, email=reset_in.email)

    if account:
        reset_in = PasswordResetTokenCreate(**{"email": account.email})

        instance = await create_reset(session=session, reset_in=reset_in)

        url = await generate_password_reset_url(
            account=account, request=request, token=instance.token
        )

        task_id = send_mail_reset_password.delay(
            account_id=account.id,
            name=account.name,
            email=account.email,
            url=url,
        )

        logger.info(
            "Password reset token created successfully with={}".format(
                {
                    "user_id": account.id,
                    "reset_id": instance.id,
                    "task_id": task_id,
                    "expire_at": instance.expire_at,
                }
            )
        )

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED)


@router.get(
    "/accounts/password-reset-form",
    summary="Form to reset password to the given token.",
    response_class=HTMLResponse,
)
@router.post(
    "/accounts/password-reset-form",
    summary="Reset password to the given token.",
    response_class=HTMLResponse,
)
@csrf_protect
async def password_reset_form(
    *,
    session: AsyncSession = Depends(get_session),
    request: Request,
    email: str,
    token: str,
):
    """Form to reset password to the given token."""
    from app.main import templates

    logger.info("Starting show form password reset")

    settings = get_settings()

    is_valid = await is_valid_token(
        session=session,
        token=token,
        email=email,
    )

    if is_valid:
        form = await PasswordResetForm.from_formdata(request)
        if request.method.lower() == "post":
            if await form.validate():
                account = await get_by_email(session=session, email=email)

                account_in = AccountUpdate(**{"password": form.password.data})

                await update(
                    session=session, account=account, account_in=account_in
                )

                logger.info(
                    "Account password updated successfully with={}".format(
                        {"user_id": account.id}
                    )
                )

                return templates.TemplateResponse(
                    "show_message.html",
                    {
                        "request": request,
                        "datetime": datetime,
                        "color": "green",
                        "message": "Password changed successfully!",
                        "app_title": settings.APP_TITLE,
                    },
                )
            else:
                for (k, v) in form.errors.items():
                    form[k].render_kw.update(
                        {"class": "form-control is-invalid"}
                    )
        else:
            return templates.TemplateResponse(
                "password_reset_form.html",
                {
                    "request": request,
                    "datetime": datetime,
                    "form": form,
                    "app_title": settings.APP_TITLE,
                },
            )

    return templates.TemplateResponse(
        "show_message.html",
        {
            "request": request,
            "datetime": datetime,
            "color": "red",
            "message": "Error occurred, please try again later!",
            "app_title": settings.APP_TITLE,
        },
    )
