import pytest

from app.account import services
from app.account.schemas import Account, AccountCreate, AccountUpdate
from app.database import async_session
from app.oauth.services import authenticate_user


@pytest.mark.asyncio
async def test_account_service_should_create(app, account_create):
    """Test account service should create."""

    async with async_session() as session:
        account = await services.create(
            session=session, account_in=AccountCreate(**account_create)
        )

    assert account.id is not None


@pytest.mark.asyncio
async def test_account_service_not_should_create_duplicated(
    app, account_create
):
    """Test account service not should create duplicated."""

    async with async_session() as session:
        await services.create(
            session=session, account_in=AccountCreate(**account_create)
        )

    with pytest.raises(Exception):
        async with async_session() as session:
            await services.create(
                session=session, account_in=AccountCreate(**account_create)
            )


@pytest.mark.asyncio
async def test_account_service_should_update(
    app, account_create, account_update
):
    """Test account service should update."""

    async with async_session() as session:
        account = await services.create(
            session=session, account_in=AccountCreate(**account_create)
        )

    schema_update = AccountUpdate(**account_update)
    data_update = schema_update.dict()

    async with async_session() as session:
        instance = await services.update(
            session=session, account=account, account_in=schema_update
        )

    updated = Account(**instance.to_dict()).dict()

    password = account_update["password"]
    account_update.pop("password")

    for field in account_update:
        assert data_update[field] == updated[field]

    async with async_session() as session:
        user = await authenticate_user(
            session=session,
            username=account_update["email"],
            password=password,
        )
    assert user.id is not None
