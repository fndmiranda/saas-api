import pytest

from app.account import services
from app.account.schemas import AccountCreate
from app.database import async_session
from app.oauth.services import authenticate_user


@pytest.mark.asyncio
async def test_oauth_service_should_authenticate_user(app, account_create):
    """Test oauth service should authenticate user."""

    async with async_session() as session:
        await services.create(
            session=session,
            account_in=AccountCreate(**account_create),
            email_verified=True,
        )

    user = await authenticate_user(
        session=session,
        username=account_create["email"],
        password=account_create["password"],
    )
    assert user is not False


@pytest.mark.asyncio
async def test_oauth_service_not_should_authenticate_user(app, account_create):
    """Test oauth service not should authenticate user."""

    async with async_session() as session:
        await services.create(
            session=session, account_in=AccountCreate(**account_create)
        )

    user = await authenticate_user(
        session=session,
        username=account_create["email"],
        password="invalid",
    )
    assert user is False
