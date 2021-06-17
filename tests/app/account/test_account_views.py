import pytest
from fastapi import status
from httpx import AsyncClient

from app.main import api_router


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
