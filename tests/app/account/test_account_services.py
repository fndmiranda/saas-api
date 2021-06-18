import pytest

from app.account.schemas import AccountCreate
from app.database import async_session
from app.account import services


@pytest.mark.asyncio
async def test_account_service_not_should_create_duplicated(
    app, account_create_body
):
    """Test account service not should create duplicated."""

    async with async_session() as session:
        await services.create(
            session=session, account=AccountCreate(**account_create_body)
        )

    with pytest.raises(Exception):
        async with async_session() as session:
            await services.create(
                session=session, account=AccountCreate(**account_create_body)
            )
