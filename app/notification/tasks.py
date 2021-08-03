import asyncio
import logging

from app.notification.services import (
    AccountNotification,
    AccountNotificationEmail,
)
from app.worker import celery

logger = logging.getLogger(__name__)


@celery.task()
def send_mail_reset_password(*, account_id: int, url: str):
    logger.info(
        "Start processing send email password reset with={}".format(
            {
                "user_id": account_id,
            }
        )
    )

    notification = AccountNotification(AccountNotificationEmail())
    asyncio.run(
        notification.send_info_reset_password(account_id=account_id, url=url)
    )


@celery.task()
def send_mail_verification(*, account_id: int, url: str):
    logger.info(
        "Start processing send email verification with={}".format(
            {
                "user_id": account_id,
            }
        )
    )

    notification = AccountNotification(AccountNotificationEmail())
    asyncio.run(
        notification.send_email_verification(account_id=account_id, url=url)
    )
