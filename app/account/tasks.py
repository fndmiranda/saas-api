import asyncio
import logging

from app.account.services import password
from app.worker import celery

logger = logging.getLogger(__name__)


@celery.task()
def send_mail_reset_password(
    *, account_id: int, name: str, email: str, url: str
):
    logger.info(
        "Start processing send email password reset with={}".format({
            "user_id": account_id,
        })
    )

    asyncio.run(password.send_mail_reset_password(
        account_id=account_id, name=name, email=email, url=url
    ))
