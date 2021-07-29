from datetime import datetime

import pytest
from fastapi import status
from httpx import AsyncClient

from app.account.services.account import get
from app.account.services.verified import get_signature
from app.auth.services import create_access_token
from app.database import async_session
from app.main import api_router
from tests.app.user.factories import UserFactory


@pytest.mark.asyncio
@pytest.mark.parametrize("email_verified_at", [None, datetime.now()])
async def test_account_view_should_check_email_verified(
    client: AsyncClient, email_verified_at
):
    """Test account view should check email verified."""
    user = await UserFactory.create(email_verified_at=email_verified_at)
    token = await create_access_token(user=user)

    response = await client.get(
        api_router.url_path_for("email_verified"),
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    if email_verified_at is not None:
        assert response.status_code == status.HTTP_200_OK
    else:
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_account_view_should_email_verify(client: AsyncClient):
    """Test account view should email verify."""
    user = await UserFactory.create(email_verified_at=None)
    token = await create_access_token(user=user)
    signature = await get_signature(account=user)

    await client.get(
        api_router.url_path_for(
            "email_verify",
            user_id=user.id,
            signature=signature,
        ),
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    async with async_session() as session:
        account = await get(session=session, account_id=user.id)
        assert account.email_verified_at is not None


@pytest.mark.asyncio
@pytest.mark.parametrize("email_verified_at", [None, datetime.now()])
async def test_account_view_should_resend_email_verified(
    client: AsyncClient, email_verified_at
):
    """Test account view should resend email verified."""
    user = await UserFactory.create(email_verified_at=email_verified_at)
    token = await create_access_token(user=user)

    response = await client.get(
        api_router.url_path_for("resend_email_verified"),
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    if email_verified_at is not None:
        assert response.status_code == status.HTTP_200_OK
    else:
        assert response.status_code == status.HTTP_201_CREATED
