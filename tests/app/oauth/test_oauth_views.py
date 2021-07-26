import pytest
from fastapi import status
from httpx import AsyncClient

from app.account.services.account import create
from app.account.schemas import AccountCreate
from app.database import async_session
from app.main import api_router


@pytest.mark.asyncio
async def test_oauth_view_should_create_token(
    client: AsyncClient, account_primary
):
    """Test oauth view should create token."""

    async with async_session() as session:
        await create(
            session=session, account_in=AccountCreate(**account_primary)
        )

    data = {
        "username": account_primary["email"],
        "password": account_primary["password"],
        "grant_type": "password",
    }

    response = await client.post(
        api_router.url_path_for("create_token"), data=data
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["access_token"] is not None
    assert response.json()["token_type"].lower() == "bearer"


@pytest.mark.asyncio
async def test_oauth_view_not_should_create_token(
    client: AsyncClient, account_primary
):
    """Test oauth view not should create token."""

    async with async_session() as session:
        await create(
            session=session, account_in=AccountCreate(**account_primary)
        )

    data = {
        "username": account_primary["email"],
        "password": "invalid",
        "grant_type": "password",
    }

    response = await client.post(
        api_router.url_path_for("create_token"), data=data
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect username or password"}
