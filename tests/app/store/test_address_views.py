import json
from datetime import datetime

import pytest
from fastapi import status
from httpx import AsyncClient

from app.auth.services import create_access_token
from app.database import async_session
from app.main import api_router
from app.store.models import StorePerson
from app.store.services.store import get
from tests.app.address.factories import AddressFactory
from tests.app.store.factories import StoreFactory
from tests.app.user.factories import UserFactory


@pytest.mark.asyncio
@pytest.mark.parametrize("email_verified_at", [None, datetime.now()])
async def test_store_view_should_create_address(
    client: AsyncClient, email_verified_at
):
    """Test store view should create store address by owner."""
    user = await UserFactory.create(email_verified_at=email_verified_at)
    store = await StoreFactory.create(
        people=[StorePerson(is_owner=True, user=user)]
    )
    token = await create_access_token(user=user)

    build = await AddressFactory.build()

    data = {
        "name": build.name,
        "is_default": build.is_default,
        "street": build.street,
        "neighborhood": build.neighborhood,
        "city": build.city,
        "postcode": build.postcode,
        "state": build.state,
        "number": build.number,
        "complement": build.complement,
        "lat": build.lat,
        "lng": build.lng,
    }

    response = await client.post(
        api_router.url_path_for("create_store_address", store_id=store.id),
        headers={"Authorization": f"Bearer {token['access_token']}"},
        json=data,
    )

    if email_verified_at is not None:
        assert response.status_code == status.HTTP_201_CREATED

        async with async_session() as session:
            store = await get(session=session, store_id=store.id)
            assert store.addresses[0].postcode == data["postcode"]
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.parametrize("is_admin", [False, True])
async def test_store_view_should_admin_create_address(
    client: AsyncClient, is_admin
):
    """Test store view should create store address by admin."""
    user = await UserFactory.create(is_admin=is_admin)
    owner = await UserFactory.create()
    store = await StoreFactory.create(
        people=[StorePerson(is_owner=True, user=owner)]
    )
    token = await create_access_token(user=user)

    build = await AddressFactory.build()

    data = {
        "name": build.name,
        "is_default": build.is_default,
        "street": build.street,
        "neighborhood": build.neighborhood,
        "city": build.city,
        "postcode": build.postcode,
        "state": build.state,
        "number": build.number,
        "complement": build.complement,
        "lat": build.lat,
        "lng": build.lng,
    }

    response = await client.post(
        api_router.url_path_for("create_store_address", store_id=store.id),
        headers={"Authorization": f"Bearer {token['access_token']}"},
        json=data,
    )

    if is_admin:
        assert response.status_code == status.HTTP_201_CREATED
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.parametrize("email_verified_at", [None, datetime.now()])
async def test_store_view_should_get_addresses(
    client: AsyncClient, email_verified_at
):
    """Test store view should get store addresses."""
    user = await UserFactory.create(email_verified_at=email_verified_at)
    token = await create_access_token(user=user)
    store = await StoreFactory.create()
    addresses = await AddressFactory.create_batch(
        3,
        parent_id=store.id,
        discriminator=store.__class__.__name__.lower(),
        state="MG",
    )

    filter_spec = [
        {
            "model": "Address",
            "field": "state",
            "op": "eq",
            "value": "MG",
        }
    ]
    sort_spec = [{"model": "Address", "field": "id", "direction": "desc"}]

    response = await client.get(
        api_router.url_path_for("get_store_addresses", store_id=store.id),
        headers={"Authorization": f"Bearer {token['access_token']}"},
        params={
            "filter": json.dumps(filter_spec),
            "sort": json.dumps(sort_spec),
        },
    )

    if email_verified_at is not None:
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["total"] == len(addresses)
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.parametrize("email_verified_at", [None, datetime.now()])
async def test_store_view_should_get_address(
    client: AsyncClient, email_verified_at
):
    """Test store view should get address."""
    owner = await UserFactory.create()
    user = await UserFactory.create(email_verified_at=email_verified_at)
    token = await create_access_token(user=user)

    store = await StoreFactory.create(
        people=[StorePerson(is_owner=True, user=owner)]
    )
    address = await AddressFactory.create(
        parent_id=store.id,
        discriminator=store.__class__.__name__.lower(),
    )

    response = await client.get(
        api_router.url_path_for(
            "get_store_address", address_id=address.id, store_id=store.id
        ),
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    if email_verified_at is not None:
        assert response.status_code == status.HTTP_200_OK
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.parametrize("email_verified_at", [None, datetime.now()])
async def test_store_view_should_update_address(
    client: AsyncClient, email_verified_at
):
    """Test store view should update store by owner."""
    user = await UserFactory.create(email_verified_at=email_verified_at)
    token = await create_access_token(user=user)

    store = await StoreFactory.create(
        people=[StorePerson(is_owner=True, user=user)]
    )
    address = await AddressFactory.create(
        parent_id=store.id,
        discriminator=store.__class__.__name__.lower(),
    )

    build = await AddressFactory.build()
    data = {
        "name": build.name,
        "is_default": build.is_default,
        "street": build.street,
        "neighborhood": build.neighborhood,
        "city": build.city,
        "postcode": build.postcode,
        "state": build.state,
        "number": build.number,
        "complement": build.complement,
        "lat": build.lat,
        "lng": build.lng,
    }

    response = await client.put(
        api_router.url_path_for(
            "update_store_address", store_id=store.id, address_id=address.id
        ),
        headers={"Authorization": f"Bearer {token['access_token']}"},
        json=data,
    )

    if email_verified_at is not None:
        assert response.status_code == status.HTTP_200_OK
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.parametrize("is_admin", [False, True])
async def test_store_view_should_admin_update_address(
    client: AsyncClient, is_admin
):
    """Test store view should update store by admin."""
    owner = await UserFactory.create()
    user = await UserFactory.create(is_admin=is_admin)
    token = await create_access_token(user=user)

    store = await StoreFactory.create(
        people=[StorePerson(is_owner=True, user=owner)]
    )
    address = await AddressFactory.create(
        parent_id=store.id,
        discriminator=store.__class__.__name__.lower(),
    )

    build = await AddressFactory.build()
    data = {
        "name": build.name,
        "is_default": build.is_default,
        "street": build.street,
        "neighborhood": build.neighborhood,
        "city": build.city,
        "postcode": build.postcode,
        "state": build.state,
        "number": build.number,
        "complement": build.complement,
        "lat": build.lat,
        "lng": build.lng,
    }

    response = await client.put(
        api_router.url_path_for(
            "update_store_address", store_id=store.id, address_id=address.id
        ),
        headers={"Authorization": f"Bearer {token['access_token']}"},
        json=data,
    )

    if is_admin:
        assert response.status_code == status.HTTP_200_OK
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.parametrize("email_verified_at", [None, datetime.now()])
async def test_store_view_should_delete_address(
    client: AsyncClient, email_verified_at
):
    """Test store view should delete address by owner."""
    user = await UserFactory.create(email_verified_at=email_verified_at)
    token = await create_access_token(user=user)
    store = await StoreFactory.create(
        people=[StorePerson(is_owner=True, user=user)]
    )
    address = await AddressFactory.create(
        parent_id=store.id,
        discriminator=store.__class__.__name__.lower(),
    )

    response = await client.delete(
        api_router.url_path_for(
            "delete_store_address", store_id=store.id, address_id=address.id
        ),
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    if email_verified_at is not None:
        assert response.status_code == status.HTTP_204_NO_CONTENT
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.parametrize("is_admin", [False, True])
async def test_store_view_should_admin_delete_address(
    client: AsyncClient, is_admin
):
    """Test store view should delete address by owner."""
    owner = await UserFactory.create()
    user = await UserFactory.create(is_admin=is_admin)
    token = await create_access_token(user=user)
    store = await StoreFactory.create(
        people=[StorePerson(is_owner=True, user=owner)]
    )
    address = await AddressFactory.create(
        parent_id=store.id,
        discriminator=store.__class__.__name__.lower(),
    )

    response = await client.delete(
        api_router.url_path_for(
            "delete_store_address", store_id=store.id, address_id=address.id
        ),
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    if is_admin:
        assert response.status_code == status.HTTP_204_NO_CONTENT
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN
