import pytest

from app.account.schemas import AccountCreate
from app.database import async_session
from app.user.services import UserService


@pytest.mark.asyncio
async def test_user_service_not_should_create_user_duplicated(
    app, account_create_body
):
    """Test user service not should create user duplicated."""

    async with async_session() as session:
        await UserService().create(
            session=session, account=AccountCreate(**account_create_body)
        )

    with pytest.raises(Exception):
        async with async_session() as session:
            await UserService().create(
                session=session, account=AccountCreate(**account_create_body)
            )
