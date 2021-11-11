from datetime import datetime, timedelta
from secrets import token_urlsafe

from fastapi import Request
from fastapi.logger import logger
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.account.schemas import PasswordResetTokenCreate
from app.config import get_settings
from app.user.models import PasswordReset, User


async def create_reset(
    session: AsyncSession,
    reset_in: PasswordResetTokenCreate,
):
    """Create a new account password reset."""
    create_data = reset_in.dict()
    settings = get_settings()

    create_data.update(
        {
            "token": token_urlsafe(64),
            "expire_at": datetime.now()
            + timedelta(minutes=settings.PASSWORD_RESET_EXPIRE_MINUTES),
        }
    )

    instance = PasswordReset(**create_data)
    session.add(instance)
    await session.commit()

    return instance


async def is_valid_token(session: AsyncSession, token: str, email: str):
    """Check if password reset token is valid."""
    query = await session.execute(
        select(PasswordReset)
        .where(
            PasswordReset.token == token,
            PasswordReset.email == email,
            PasswordReset.expire_at >= datetime.now(),
        )
        .with_only_columns(func.count())
    )

    is_valid = query.scalar_one()
    await session.commit()

    return bool(is_valid)


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


async def generate_password_reset_url(
    *, account: User, request: Request, token: str
):
    """Generate password reset url."""
    logger.info(
        "Starting generate password reset url with={}".format(
            {
                "user_id": account.id,
            }
        )
    )

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
    return url
