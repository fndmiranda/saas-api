import pytest
from fastapi import status
from httpx import AsyncClient

from app.account.schemas import AccountCreate
from app.database import async_session
from app.main import api_router
from app.account import services


@pytest.mark.asyncio
async def test_oauth_view_should_create_token(
    client: AsyncClient, account_create_body
):
    """Test oauth view should create token."""

    async with async_session() as session:
        await services.create(
            session=session, account=AccountCreate(**account_create_body)
        )

    data = {
        "username": account_create_body["email"],
        "password": account_create_body["password"],
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
    client: AsyncClient, account_create_body
):
    """Test oauth view not should create token."""

    async with async_session() as session:
        await services.create(
            session=session, account=AccountCreate(**account_create_body)
        )

    data = {
        "username": account_create_body["email"],
        "password": "invalid",
        "grant_type": "password",
    }

    response = await client.post(
        api_router.url_path_for("create_token"), data=data
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect username or password"}
