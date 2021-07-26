import pprint

import pytest
from fastapi import status, Request

from app.account.services.account import create, update
from app.account.schemas import Account, AccountCreate, AccountUpdate
from app.account.services.password import send_mail_reset_password, \
    generate_password_reset_url
from app.auth.services import authenticate_user
from app.database import async_session
from httpx import AsyncClient

from tests.app.user.factories import UserFactory
from tests.utils import vcr


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

    async with async_session() as session:
        instance = await update(
            session=session, account=account, account_in=schema_update
        )

    updated = Account(**instance.dict()).dict()

    password = account_secondary["password"]
    account_secondary.pop("password")

    for field in account_secondary:
        assert data_update[field] == updated[field]

    async with async_session() as session:
        user = await authenticate_user(
            session=session,
            username=account_secondary["email"],
            password=password,
        )
    assert user.id is not None


@pytest.mark.asyncio
@vcr.use_cassette()
async def test_account_service_should_send_mail_reset_password(
        client: AsyncClient
):
    """Test account service should send mail reset password."""

    user = await UserFactory.create()

    response = await send_mail_reset_password(
        account_id=user.id, name=user.name, email=user.email, url="testing_url"
    )

    assert response.status_code == status.HTTP_202_ACCEPTED
