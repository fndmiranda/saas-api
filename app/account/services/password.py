import pprint
from datetime import datetime, timedelta
from secrets import token_urlsafe
from typing import Optional

import requests
from fastapi import Request

from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.account.schemas import AccountCreate, AccountUpdate, \
    PasswordResetCreate
from app.address.models import Address
from app.config import get_settings
from app.user.models import User, PasswordReset
import httpx
import asyncio


async def create_reset(
    session: AsyncSession,
    reset_in: PasswordResetCreate,
):
    """Create a new account password reset."""
    create_data = reset_in.dict()

    instance = PasswordReset(**create_data)
    session.add(instance)
    await session.commit()

    return instance


async def send_mail_reset_password(
    *, account_id: int, name: str, email: str, url: str
):
    logger.info(
        "Start send mail to account reset password with={}".format({
            "user_id": account_id,
        })
    )

    settings = get_settings()

    kwargs = {
        "url": url,
        "template_name": "password_reset_token_email.html",
        "subject": "Notificação de redefinição de senha",
        "expire_minutes": settings.PASSWORD_RESET_EXPIRE_MINUTES,
        "button_title": "Redefinir senha",
    }

    data = await _get_payload_send_email(
        name=name, email=email, **kwargs,
    )

    async with httpx.AsyncClient() as client:
        pass
        # response = await client.post(
        #     settings.SENDGRID_API_URL,
        #     json=data,
        #     headers={
        #         "Authorization": f"Bearer {settings.SENDGRID_API_KEY}",
        #         "Content-Type": "application/json",
        #     },
        # )
        #
        # logger.info(
        #     "Sent account email password reset token with={}".format({
        #         "user_id": account_id,
        #     })
        # )
        #
        # return response


async def _get_payload_send_email(name: str, email: str, **kwargs):
    """Get payload email to send."""
    from app.main import templates
    settings = get_settings()

    kwargs.setdefault("type", "text/html")
    kwargs.setdefault("app_title", settings.APP_TITLE)
    kwargs.setdefault("datetime", datetime)

    return {
        "personalizations": [
            {
                "to": [{"email": email, "name": name}],
                "subject": kwargs["subject"],
            }
        ],
        "from": {
            "email": settings.MAIL_DEFAULT_FROM_EMAIL,
            "name": settings.MAIL_DEFAULT_FROM_NAME,
        },
        "reply_to": {
            "email": settings.MAIL_DEFAULT_FROM_EMAIL,
            "name": settings.MAIL_DEFAULT_FROM_NAME,
        },
        "content": [
            {
                "type": kwargs["type"],
                "value": templates.get_template(
                    "password_reset_token_email.html"
                ).render(kwargs),
            }
        ],
    }


async def generate_password_reset_url(
        *, account: User, request: Request
):
    """Generate password reset url"""
    logger.info(
        "Starting generate password reset url with={}".format({
            "user_id": account.id,
        })
    )

    token = token_urlsafe(64)

    url = "{}/?email={}&token={}".format(
        request.url_for("password_reset_form"), account.email, token
    )

    logger.info(
        "Password reset url generated successfully with={}".format(
            {
                "user_id": account.id,
            }
        )
    )
    return url, token
