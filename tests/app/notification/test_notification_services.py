import pytest
from fastapi import status
from httpx import AsyncClient

from app.notification.services import (
    AccountNotification,
    AccountNotificationEmail,
)
from tests.app.user.factories import UserFactory
from tests.utils import vcr


@pytest.mark.asyncio
@vcr.use_cassette()
async def test_notification_service_should_send_info_reset_password(
    client: AsyncClient,
):
    """Test account notification service should send info to reset password."""

    user = await UserFactory.create(email_verified_at=None)

    notification = AccountNotification(AccountNotificationEmail())
    response = await notification.send_info_reset_password(
        account_id=user.id, url="testing_url"
    )

    assert response.status_code == status.HTTP_202_ACCEPTED


@pytest.mark.asyncio
@vcr.use_cassette()
async def test_notification_service_should_send_email_verification(
    client: AsyncClient,
):
    """Test account notification service should send email verification."""

    user = await UserFactory.create(email_verified_at=None)

    notification = AccountNotification(AccountNotificationEmail())
    response = await notification.send_email_verification(
        account_id=user.id, url="testing_url"
    )

    assert response.status_code == status.HTTP_202_ACCEPTED
