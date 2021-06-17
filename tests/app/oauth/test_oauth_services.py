import pytest

from app.account.schemas import AccountCreate
from app.database import async_session
from app.oauth.services import authenticate_user
from app.user.services import UserService


@pytest.mark.asyncio
async def test_oauth_service_should_authenticate_user(
    app, account_create_body
):
    """Test oauth service should authenticate user."""

    async with async_session() as session:
        await UserService().create(
            session=session, account=AccountCreate(**account_create_body)
        )

    user = await authenticate_user(
        session=session,
        username=account_create_body["email"],
        password=account_create_body["password"],
    )
    assert user is not False


@pytest.mark.asyncio
async def test_oauth_service_not_should_authenticate_user(
    app, account_create_body
):
    """Test oauth service not should authenticate user."""

    async with async_session() as session:
        await UserService().create(
            session=session, account=AccountCreate(**account_create_body)
        )

    user = await authenticate_user(
        session=session,
        username=account_create_body["email"],
        password="invalid",
    )
    assert user is False
