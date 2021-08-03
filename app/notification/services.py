from __future__ import annotations

import logging
from abc import ABCMeta, abstractmethod
from datetime import datetime

import httpx

from app.account.services.account import get
from app.config import get_settings
from app.database import async_session

logger = logging.getLogger(__name__)


class AccountNotification:
    """Define the interface of account notification."""

    def __init__(self, strategy):
        self._strategy = strategy

    async def send_info_reset_password(self, account_id: int, url: str):
        """Send information to reset account password."""

        return await self._strategy.send_info_reset_password(
            account_id=account_id,
            url=url,
        )

    async def send_email_verification(self, account_id: int, url: str):
        """Send email to verification email account."""

        return await self._strategy.send_email_verification(
            account_id=account_id,
            url=url,
        )


class AccountNotificationStrategy(metaclass=ABCMeta):
    """Interface common to all supported notification."""

    @abstractmethod
    async def send_info_reset_password(self, account_id: int, url: str):
        pass

    @abstractmethod
    async def send_email_verification(self, account_id: int, url: str):
        pass


class AccountNotificationEmail(AccountNotificationStrategy):
    async def send_info_reset_password(self, account_id: int, url: str):
        """Send email information to reset account password."""

        logger.info(
            "Start send mail to account reset password with={}".format(
                {
                    "user_id": account_id,
                }
            )
        )

        settings = get_settings()

        async with async_session() as session:
            account = await get(session=session, account_id=account_id)

            kwargs = {
                "url": url,
                "template_name": "password_reset_token_email.html",
                "subject": "Notificação de redefinição de senha",
                "expire_minutes": settings.PASSWORD_RESET_EXPIRE_MINUTES,
                "button_title": "Redefinir senha",
            }

            data = await self.get_payload_send_email(
                name=account.name,
                email=account.email,
                **kwargs,
            )

            response = await self.send_email(data=data)

            logger.info(
                "Sent account email password reset token with={}".format(
                    {
                        "user_id": account_id,
                    }
                )
            )

            return response

    async def send_email_verification(self, account_id: int, url: str):
        """Send email to verification email account."""

        logger.info(
            "Start send email to verification email account with={}".format(
                {
                    "user_id": account_id,
                }
            )
        )

        async with async_session() as session:
            account = await get(session=session, account_id=account_id)

            kwargs = {
                "url": url,
                "template_name": "resend_verify_email.html",
                "subject": "Check email address",
                "button_title": "Check email address",
            }

            data = await self.get_payload_send_email(
                name=account.name,
                email=account.email,
                **kwargs,
            )

            response = await self.send_email(data=data)

            logger.info(
                "Sent verification email account with={}".format(
                    {
                        "user_id": account_id,
                    }
                )
            )

            return response

    async def send_email(self, data: dict):
        """Send email."""

        settings = get_settings()

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    settings.SENDGRID_API_URL,
                    json=data,
                    headers={
                        "Authorization": f"Bearer {settings.SENDGRID_API_KEY}",
                        "Content-Type": "application/json",
                    },
                )

                # Raise for HTTP status code
                response.raise_for_status()
            except httpx.HTTPError as e:
                logger.error(
                    "Error to send email with={}".format(
                        {
                            "error": str(e),
                        }
                    )
                )
                raise Exception(str(e))

            return response

    async def get_payload_send_email(self, name: str, email: str, **kwargs):
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
