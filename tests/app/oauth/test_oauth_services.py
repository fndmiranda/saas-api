import pytest

from app.account import services
from app.account.schemas import AccountCreate
from app.auth.services import authenticate_user
from app.database import async_session


@pytest.mark.asyncio
async def test_oauth_service_should_authenticate_user(app, account_primary):
    """Test oauth service should authenticate user."""

    async with async_session() as session:
        await services.create(
            session=session,
            account_in=AccountCreate(**account_primary),
            email_verified=True,
        )

    user = await authenticate_user(
        session=session,
        username=account_primary["email"],
        password=account_primary["password"],
    )
    assert user is not False


@pytest.mark.asyncio
async def test_oauth_service_not_should_authenticate_user(
    app, account_primary
):
    """Test oauth service not should authenticate user."""

    async with async_session() as session:
        await services.create(
            session=session, account_in=AccountCreate(**account_primary)
        )

    user = await authenticate_user(
        session=session,
        username=account_primary["email"],
        password="invalid",
    )
    assert user is False
