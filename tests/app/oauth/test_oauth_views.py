import pytest
from fastapi import status
from httpx import AsyncClient

from app.main import api_router
from tests.app.user.factories import UserFactory


@pytest.mark.asyncio
async def test_oauth_view_should_create_token(
    client: AsyncClient, account_primary
):
    """Test oauth view should create token."""
    user = await UserFactory.create(password="testpass")

    data = {
        "username": user.email,
        "password": "testpass",
        "grant_type": "password",
    }

    response = await client.post(
        api_router.url_path_for("create_token"), data=data
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["access_token"] is not None
    assert response.json()["token_type"].lower() == "bearer"


@pytest.mark.asyncio
async def test_oauth_view_not_should_create_token(client: AsyncClient):
    """Test oauth view not should create token."""
    user = await UserFactory.create()

    data = {
        "username": user.email,
        "password": "invalid",
        "grant_type": "password",
    }

    response = await client.post(
        api_router.url_path_for("create_token"), data=data
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect username or password"}
