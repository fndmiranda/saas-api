from unittest.mock import patch

import pytest
from httpx import AsyncClient

from tests.app.user.factories import UserFactory


@pytest.mark.asyncio
@patch("app.notification.tasks.send_mail_reset_password.run")
async def test_notification_task_should_send_mail_reset_password(
    mock_run, client: AsyncClient
):
    """Test account notification task should send mail to reset password."""

    user1 = await UserFactory.create()
    user2 = await UserFactory.create()

    assert mock_run.run(
        account_id=user1.id,
        url="testing_url1",
    )
    mock_run.run.assert_called_once_with(
        account_id=user1.id,
        url="testing_url1",
    )

    assert mock_run.run(
        account_id=user2.id,
        url="testing_url2",
    )
    assert mock_run.run.call_count == 2


@pytest.mark.asyncio
@patch("app.notification.tasks.send_mail_verification.run")
async def test_notification_task_should_send_mail_verification(
    mock_run, client: AsyncClient
):
    user1 = await UserFactory.create()
    user2 = await UserFactory.create()

    assert mock_run.run(
        account_id=user1.id,
        name=user1.name,
        email=user1.email,
        url="testing_url1",
    )
    mock_run.run.assert_called_once_with(
        account_id=user1.id,
        name=user1.name,
        email=user1.email,
        url="testing_url1",
    )

    assert mock_run.run(
        account_id=user2.id,
        name=user2.name,
        email=user2.email,
        url="testing_url2",
    )
    assert mock_run.run.call_count == 2
