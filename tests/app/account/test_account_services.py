import pytest

from app.account.schemas import Account, AccountCreate, AccountUpdate
from app.account.services.account import create, update
from app.auth.services import authenticate_user
from app.database import async_session


@pytest.mark.asyncio
async def test_account_service_should_create(app, account_primary):
    """Test account service should create."""
    async with async_session() as session:
        account = await create(
            session=session, account_in=AccountCreate(**account_primary)
        )

        assert account.id is not None


@pytest.mark.asyncio
async def test_account_service_not_should_create_duplicated(
    app, account_primary
):
    """Test account service not should create duplicated."""

    async with async_session() as session:
        await create(
            session=session, account_in=AccountCreate(**account_primary)
        )

    with pytest.raises(Exception):
        async with async_session() as session:
            await create(
                session=session, account_in=AccountCreate(**account_primary)
            )


@pytest.mark.asyncio
async def test_account_service_should_update(
    app, account_primary, account_secondary
):
    """Test account service should update."""
    async with async_session() as session:
        account = await create(
            session=session, account_in=AccountCreate(**account_primary)
        )

        schema_update = AccountUpdate(**account_secondary)
        data_update = schema_update.dict()

        instance = await update(
            session=session, account=account, account_in=schema_update
        )

        updated = Account(**instance.dict()).dict()

        password = account_secondary["password"]
        account_secondary.pop("password")

        for field in account_secondary:
            assert data_update[field] == updated[field]

        user = await authenticate_user(
            session=session,
            username=account_secondary["email"],
            password=password,
        )
        assert user is not False
