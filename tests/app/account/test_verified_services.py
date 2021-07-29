import pytest
from fastapi import status
from httpx import AsyncClient

from app.account.services.verified import send_email_verification
from tests.app.user.factories import UserFactory
from tests.utils import vcr


@pytest.mark.asyncio
@vcr.use_cassette()
async def test_account_service_should_send_email_verification(
    client: AsyncClient,
):
    """Test account service should send email verification."""

    user = await UserFactory.create(email_verified_at=None)

    response = await send_email_verification(
        account_id=user.id, name=user.name, email=user.email, url="testing_url"
    )

    assert response.status_code == status.HTTP_202_ACCEPTED
