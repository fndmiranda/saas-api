import pytest
from fastapi import status
from httpx import AsyncClient

from app.account.schemas import AccountCreate
from app.database import async_session
from app.main import api_router
from app.oauth.services import create_access_token
from app.user.services import UserService


@pytest.mark.asyncio
@pytest.mark.parametrize("accept_legal_term", [True])
async def test_account_view_should_create_account(
    client: AsyncClient, accept_legal_term, account_create_body
):
    """Test account view should create account."""

    response = await client.post(
        api_router.url_path_for("create_account"), json=account_create_body
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["id"] is not None


@pytest.mark.asyncio
async def test_account_view_should_get_account(
    client: AsyncClient, account_create_body
):
    """Test account view should get account."""

    async with async_session() as session:
        user = await UserService().create(
            session=session, account=AccountCreate(**account_create_body)
        )

    token = await create_access_token(user=user)

    response = await client.get(
        api_router.url_path_for("get_account"),
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] is not None
