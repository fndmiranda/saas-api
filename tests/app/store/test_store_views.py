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
from tests.app.store.factories import SegmentFactory, StoreFactory
from tests.app.user.factories import UserFactory


@pytest.mark.asyncio
@pytest.mark.parametrize("email_verified_at", [None, datetime.now()])
async def test_store_view_should_create_store_without_addresses(
    client: AsyncClient, email_verified_at
):
    """Test store view should create store without addresses."""
    segment = await SegmentFactory.create()
    user = await UserFactory.create(email_verified_at=email_verified_at)
    token = await create_access_token(user=user)

    build = await StoreFactory.build()

    data = {
        "title": build.title,
        "legal": build.legal,
        "phones": build.phones,
        "information": build.information,
        "is_active": build.is_active,
        "document_type": build.document_type,
        "document_number": build.document_number,
        "segment_id": segment.id,
    }

    response = await client.post(
        api_router.url_path_for("create_store"),
        json=data,
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    if email_verified_at is not None:
        assert response.status_code == status.HTTP_201_CREATED

        async with async_session() as session:
            store = await get(session=session, store_id=response.json()["id"])

            query = await session.execute(
                store.people.where(
                    StorePerson.is_owner,
                    StorePerson.is_active,
                    StorePerson.user_id == user.id,
                )
            )
            person = query.scalar_one_or_none()
            await session.commit()

            assert person is not None
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_store_view_should_create_store_with_addresses(
    client: AsyncClient,
):
    """Test store view should create store with addresses."""
    segment = await SegmentFactory.create()
    address = await AddressFactory.build()
    user = await UserFactory.create()
    token = await create_access_token(user=user)

    build = await StoreFactory.build()

    data = {
        "title": build.title,
        "legal": build.legal,
        "phones": build.phones,
        "information": build.information,
        "is_active": build.is_active,
        "document_type": build.document_type,
        "document_number": build.document_number,
        "segment_id": segment.id,
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
        api_router.url_path_for("create_store"),
        json=data,
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_store_view_not_should_create_duplicate_store(
    client: AsyncClient,
):
    """Test store view not should create duplicate segment."""
    segment = await SegmentFactory.create()
    user = await UserFactory.create(is_admin=True)
    token = await create_access_token(user=user)

    store = await StoreFactory.create()

    data = {
        "title": store.title,
        "legal": store.legal,
        "phones": store.phones,
        "information": store.information,
        "is_active": store.is_active,
        "document_type": store.document_type,
        "document_number": store.document_number,
        "segment_id": segment.id,
    }

    response = await client.post(
        api_router.url_path_for("create_store"),
        json=data,
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_store_view_should_get_stores(client: AsyncClient):
    """Test store view should get stores."""
    stores = await StoreFactory.create_batch(3)

    filter_spec = [
        {
            "model": "Store",
            "field": "title",
            "op": "ilike",
            "value": "%store title%",
        }
    ]
    sort_spec = [{"model": "Store", "field": "id", "direction": "desc"}]

    response = await client.get(
        api_router.url_path_for("get_stores"),
        params={
            "filter": json.dumps(filter_spec),
            "sort": json.dumps(sort_spec),
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["total"] == len(stores)


@pytest.mark.asyncio
@pytest.mark.parametrize("email_verified_at", [None, datetime.now()])
async def test_store_view_should_get_store(
    client: AsyncClient, email_verified_at
):
    """Test store view should get store."""
    user = await UserFactory.create(email_verified_at=email_verified_at)
    token = await create_access_token(user=user)

    store = await StoreFactory.create()

    response = await client.get(
        api_router.url_path_for("get_store", store_id=store.id),
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    if email_verified_at is not None:
        assert response.status_code == status.HTTP_200_OK
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.parametrize("email_verified_at", [None, datetime.now()])
async def test_store_view_should_update_store(
    client: AsyncClient, email_verified_at
):
    """Test store view should update store by owner."""
    user = await UserFactory.create(email_verified_at=email_verified_at)
    token = await create_access_token(user=user)

    store = await StoreFactory.create(
        people=[StorePerson(is_owner=True, user=user)]
    )
    build = await StoreFactory.build()
    data = {
        "title": build.title,
        "legal": build.legal,
        "phones": build.phones,
        "information": build.information,
        "is_active": build.is_active,
        "document_type": build.document_type,
        "document_number": build.document_number,
    }

    response = await client.put(
        api_router.url_path_for("update_store", store_id=store.id),
        headers={"Authorization": f"Bearer {token['access_token']}"},
        json=data,
    )

    if email_verified_at is not None:
        assert response.status_code == status.HTTP_200_OK
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.parametrize("is_admin", [False, True])
async def test_store_view_should_admin_update_store(
    client: AsyncClient, is_admin
):
    """Test store view should update store by admin."""
    user = await UserFactory.create(is_admin=is_admin)
    token = await create_access_token(user=user)

    owner = await UserFactory.create()
    store = await StoreFactory.create(
        people=[StorePerson(is_owner=True, user=owner)]
    )
    build = await StoreFactory.build()
    data = {
        "title": build.title,
        "legal": build.legal,
        "phones": build.phones,
        "information": build.information,
        "is_active": build.is_active,
        "document_type": build.document_type,
        "document_number": build.document_number,
    }

    response = await client.put(
        api_router.url_path_for("update_store", store_id=store.id),
        headers={"Authorization": f"Bearer {token['access_token']}"},
        json=data,
    )

    if is_admin:
        assert response.status_code == status.HTTP_200_OK
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.parametrize("email_verified_at", [None, datetime.now()])
async def test_store_view_should_delete_store(
    client: AsyncClient, email_verified_at
):
    """Test store view should delete store by owner."""
    user = await UserFactory.create(email_verified_at=email_verified_at)
    token = await create_access_token(user=user)

    store = await StoreFactory.create(
        people=[StorePerson(is_owner=True, user=user)]
    )

    response = await client.delete(
        api_router.url_path_for("delete_store", store_id=store.id),
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    if email_verified_at is not None:
        assert response.status_code == status.HTTP_204_NO_CONTENT
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.parametrize("is_admin", [True])
async def test_store_view_should_admin_delete_store(
    client: AsyncClient, is_admin
):
    """Test store view should delete store by admin."""
    owner = await UserFactory.create()
    user = await UserFactory.create(is_admin=is_admin)
    token = await create_access_token(user=user)

    store = await StoreFactory.create(
        people=[StorePerson(is_owner=True, user=owner)]
    )

    response = await client.delete(
        api_router.url_path_for("delete_store", store_id=store.id),
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    if is_admin:
        assert response.status_code == status.HTTP_204_NO_CONTENT
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN
