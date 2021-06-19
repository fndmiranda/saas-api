import pytest
from fastapi import status
from httpx import AsyncClient

from app.account import services
from app.account.schemas import AccountCreate
from app.database import async_session
from app.main import api_router
from app.oauth.services import create_access_token
from app.user.models import User


@pytest.mark.asyncio
@pytest.mark.parametrize("accept_legal_term", [True])
async def test_account_view_should_create_account(
    client: AsyncClient, accept_legal_term, account_create
):
    """Test account view should create account."""

    response = await client.post(
        api_router.url_path_for("create_account"), json=account_create
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["id"] is not None


@pytest.mark.asyncio
async def test_account_view_should_get_account(
    client: AsyncClient, account_create
):
    """Test account view should get account."""

    async with async_session() as session:
        account = await services.create(
            session=session,
            account_in=AccountCreate(**account_create),
            email_verified=True,
        )

    token = await create_access_token(user=account)

    response = await client.get(
        api_router.url_path_for("get_account"),
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] is not None


@pytest.mark.asyncio
async def test_account_view_should_update_account(
    client: AsyncClient, account_create, account_update
):
    """Test account view should update account."""
    async with async_session() as session:
        account = await services.create(
            session=session,
            account_in=AccountCreate(**account_create),
            email_verified=True,
        )

    token = await create_access_token(user=account)

    response = await client.put(
        api_router.url_path_for("update_account"),
        headers={"Authorization": f"Bearer {token['access_token']}"},
        json=account_update,
    )

    password = account_update["password"]
    account_update.pop("password")

    for field in account_update:
        assert account_update[field] == response.json()[field]

    data = {
        "username": account_update["email"],
        "password": password,
        "grant_type": "password",
    }

    response_token = await client.post(
        api_router.url_path_for("create_token"), data=data
    )

    assert response.status_code == status.HTTP_200_OK
    assert response_token.json()["access_token"] is not None


@pytest.mark.asyncio
async def test_account_view_should_delete_account(
    client: AsyncClient, account_create, account_update
):
    """Test account view should delete account."""
    async with async_session() as session:
        account = await services.create(
            session=session,
            account_in=AccountCreate(**account_create),
            email_verified=True,
        )

    token = await create_access_token(user=account)

    response = await client.delete(
        api_router.url_path_for("update_account"),
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    async with async_session() as session:
        user = await session.get(User, account.id)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user is None
