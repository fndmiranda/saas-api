from datetime import datetime

import pytest
from fastapi import status
from httpx import AsyncClient

from app.account import services
from app.account.schemas import AccountCreate
from app.auth.services import create_access_token
from app.database import async_session
from app.main import api_router
from app.user.models import User
from tests.app.address.factories import AddressFactory
from tests.app.user.factories import UserFactory


@pytest.mark.asyncio
@pytest.mark.parametrize("accept_legal_term", [False, True])
async def test_account_view_should_create_account_without_addresses(
    client: AsyncClient, accept_legal_term
):
    """Test account view should create account without addresses."""
    build = await UserFactory.build()
    data = {
        "name": build.name,
        "email": build.email,
        "accept_legal_term": accept_legal_term,
        "nickname": build.nickname,
        "document_number": build.document_number,
        "password": "testpass",
        "birthdate": str(build.birthdate),
    }

    response = await client.post(
        api_router.url_path_for("create_account"), json=data
    )

    if accept_legal_term:
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["id"] is not None
    else:
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_account_view_should_create_account_with_addresses(
    client: AsyncClient,
):
    """Test account view should create account with addresses."""
    address = await AddressFactory.build()
    build = await UserFactory.build()
    data = {
        "name": build.name,
        "email": build.email,
        "accept_legal_term": build.accept_legal_term,
        "nickname": build.nickname,
        "document_number": build.document_number,
        "password": "testpass",
        "birthdate": str(build.birthdate),
        "addresses": [
            {
                "name": address.name,
                "is_default": address.is_default,
                "street": address.street,
                "neighborhood": address.neighborhood,
                "city": address.city,
                "postcode": address.postcode,
                "state": address.state,
                "number": address.number,
                "complement": address.complement,
                "lat": address.lat,
                "lng": address.lng,
            }
        ],
    }

    response = await client.post(
        api_router.url_path_for("create_account"), json=data
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["id"] is not None


@pytest.mark.asyncio
async def test_account_view_not_should_create_account_duplicate(
    client: AsyncClient,
):
    """Test account view not should create account duplicate."""
    build = await UserFactory.build()
    data = {
        "name": build.name,
        "email": build.email,
        "accept_legal_term": build.accept_legal_term,
        "nickname": build.nickname,
        "document_number": build.document_number,
        "password": "testpass",
        "birthdate": str(build.birthdate),
    }

    async with async_session() as session:
        await services.create(
            session=session, account_in=AccountCreate(**data)
        )

    response = await client.post(
        api_router.url_path_for("create_account"), json=data
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
@pytest.mark.parametrize("email_verified_at", [None, datetime.now()])
async def test_account_view_should_get_account(
    client: AsyncClient, email_verified_at
):
    """Test account view should get account."""

    user = await UserFactory.create(email_verified_at=email_verified_at)
    token = await create_access_token(user=user)

    response = await client.get(
        api_router.url_path_for("get_account"),
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    if email_verified_at:
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] is not None
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.parametrize("email_verified_at", [None, datetime.now()])
async def test_account_view_should_update_account(
    client: AsyncClient, email_verified_at
):
    """Test account view should update account."""
    user = await UserFactory.create(email_verified_at=email_verified_at)
    token = await create_access_token(user=user)

    build = await UserFactory.build()
    data = {
        "name": build.name,
        "email": build.email,
        "accept_legal_term": build.accept_legal_term,
        "nickname": build.nickname,
        "document_number": build.document_number,
        "password": "testpass_update",
        "birthdate": str(build.birthdate),
    }

    response = await client.put(
        api_router.url_path_for("update_account"),
        json=data,
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    if email_verified_at:
        password = data["password"]
        data.pop("password")

        for field in data:
            assert data[field] == response.json()[field]

        data = {
            "username": data["email"],
            "password": password,
            "grant_type": "password",
        }

        response_token = await client.post(
            api_router.url_path_for("create_token"), data=data
        )

        assert response.status_code == status.HTTP_200_OK
        assert response_token.json()["access_token"] is not None
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_account_view_not_should_update_account_duplicate(
    client: AsyncClient,
):
    """Test account view not should update account duplicate."""
    user = await UserFactory.create()
    owner = await UserFactory.create()
    token = await create_access_token(user=owner)

    data = {
        "name": user.name,
        "email": user.email,
        "accept_legal_term": user.accept_legal_term,
        "nickname": user.nickname,
        "document_number": user.document_number,
        "password": "testpass",
        "birthdate": str(user.birthdate),
    }

    response = await client.put(
        api_router.url_path_for("update_account"),
        headers={"Authorization": f"Bearer {token['access_token']}"},
        json=data,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
@pytest.mark.parametrize("email_verified_at", [None, datetime.now()])
async def test_account_view_should_delete_account(
    client: AsyncClient, email_verified_at
):
    """Test account view should delete account."""
    user = await UserFactory.create(email_verified_at=email_verified_at)
    token = await create_access_token(user=user)

    response = await client.delete(
        api_router.url_path_for("update_account"),
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    if email_verified_at:
        async with async_session() as session:
            user = await session.get(User, user.id)
            await session.commit()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert user is None
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN
