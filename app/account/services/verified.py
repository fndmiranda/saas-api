import hashlib
from datetime import datetime
from hmac import compare_digest

import httpx
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.account.schemas import AccountEmailVerify
from app.config import get_settings
from app.user.models import User


async def send_email_verification(
    *, account_id: int, name: str, email: str, url: str
):
    logger.info(
        "Start send mail to verification email account with={}".format(
            {
                "user_id": account_id,
            }
        )
    )

    settings = get_settings()

    kwargs = {
        "url": url,
        "template_name": "resend_verify_email.html",
        "subject": "Check email address",
        "button_title": "Check email address",
    }

    data = await get_payload_send_email(
        name=name,
        email=email,
        **kwargs,
    )

    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.SENDGRID_API_URL,
            json=data,
            headers={
                "Authorization": f"Bearer {settings.SENDGRID_API_KEY}",
                "Content-Type": "application/json",
            },
        )

        logger.info(
            "Sent verification email account with={}".format(
                {
                    "user_id": account_id,
                }
            )
        )

        return response


async def mark_email_as_verified(
    *, session: AsyncSession, account: User, verify_in: AccountEmailVerify
):
    """Mark a account email verified."""
    account_data = jsonable_encoder(account)
    update_data = verify_in.dict(exclude_unset=True)

    for field in account_data:
        if field in update_data:
            setattr(account, field, update_data[field])

    await session.commit()

    return account


async def get_signature(account: User):
    """Get the signature."""
    word = "{}-{}".format(
        account.created_at.timestamp(), account.salt
    ).encode()
    return hashlib.sha256(word).hexdigest()


async def signature_is_valid(account: User, signature: str):
    """Determine if the signature is valid."""
    return compare_digest(await get_signature(account=account), signature)


async def get_payload_send_email(name: str, email: str, **kwargs):
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
                    kwargs["template_name"]
                ).render(kwargs),
            }
        ],
    }


async def generate_verify_email_url(*, account: User, request: Request):
    """Generate verify email url."""
    logger.info(
        "Starting generate email verify url with={}".format(
            {
                "user_id": account.id,
            }
        )
    )

    url = request.url_for(
        "email_verify",
        user_id=account.id,
        signature=await get_signature(account=account),
    )

    logger.info(
        "Verify email url generated successfully with={}".format(
            {
                "user_id": account.id,
            }
        )
    )
    return url
