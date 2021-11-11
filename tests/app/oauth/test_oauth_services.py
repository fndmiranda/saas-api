import pytest

from app.account.schemas import AccountCreate
from app.account.services.account import create
from app.auth.services import authenticate_user
from app.database import async_session
from tests.app.user.factories import UserFactory


@pytest.mark.asyncio
async def test_oauth_service_should_authenticate_user(app, account_primary):
    """Test oauth service should authenticate user."""
    user = await UserFactory.create(password="testpass")

    async with async_session() as session:
        account = await authenticate_user(
            session=session,
            username=user.email,
            password="testpass",
        )
        assert account is not False


@pytest.mark.asyncio
async def test_oauth_service_not_should_authenticate_user(
    app, account_primary
):
    """Test oauth service not should authenticate user."""

    async with async_session() as session:
        await create(
            session=session, account_in=AccountCreate(**account_primary)
        )

    user = await authenticate_user(
        session=session,
        username=account_primary["email"],
        password="invalid",
    )
    assert user is False
