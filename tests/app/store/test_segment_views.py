import json
from datetime import datetime

import pytest
from fastapi import status
from httpx import AsyncClient

from app.auth.services import create_access_token
from app.main import api_router
from tests.app.store.factories import SegmentFactory
from tests.app.user.factories import UserFactory


@pytest.mark.asyncio
@pytest.mark.parametrize("is_admin", [False, True])
@pytest.mark.parametrize("email_verified_at", [None, datetime.now()])
async def test_store_view_should_create_segment(
    client: AsyncClient, is_admin, email_verified_at
):
    """Test store view should create segment only by admin."""
    user = await UserFactory.create(
        is_admin=is_admin, email_verified_at=email_verified_at
    )
    token = await create_access_token(user=user)

    build = await SegmentFactory.build()
    data = {
        "title": build.title,
        "is_active": build.is_active,
        "image": build.image,
        "color": build.color,
    }

    response = await client.post(
        api_router.url_path_for("create_segment"),
        json=data,
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    if is_admin and email_verified_at is not None:
        assert response.status_code == status.HTTP_201_CREATED
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_store_view_not_should_create_duplicate_segment(
    client: AsyncClient,
):
    """Test store view not should create duplicate segment."""
    user = await UserFactory.create(is_admin=True)
    token = await create_access_token(user=user)

    segment = await SegmentFactory.create()
    data = {
        "title": segment.title,
        "is_active": segment.is_active,
        "image": segment.image,
        "color": segment.color,
    }

    response = await client.post(
        api_router.url_path_for("create_segment"),
        json=data,
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_store_view_should_get_segments(client: AsyncClient):
    """Test store view should get segments."""
    segments = await SegmentFactory.create_batch(3)

    filter_spec = [
        {
            "model": "Segment",
            "field": "title",
            "op": "ilike",
            "value": "%segment title%",
        }
    ]
    sort_spec = [{"model": "Segment", "field": "id", "direction": "desc"}]

    response = await client.get(
        api_router.url_path_for("get_segments"),
        params={
            "filter": json.dumps(filter_spec),
            "sort": json.dumps(sort_spec),
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["total"] == len(segments)


@pytest.mark.asyncio
@pytest.mark.parametrize("email_verified_at", [None, datetime.now()])
async def test_store_view_should_get_segment(
    client: AsyncClient, email_verified_at
):
    """Test store view should get segment."""
    user = await UserFactory.create(email_verified_at=email_verified_at)
    token = await create_access_token(user=user)

    segment = await SegmentFactory.create()

    response = await client.get(
        api_router.url_path_for("get_segment", segment_id=segment.id),
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    if email_verified_at is not None:
        assert response.status_code == status.HTTP_200_OK
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_store_view_not_should_get_segment_not_found(
    client: AsyncClient,
):
    """Test store view not should get segment not found."""
    user = await UserFactory.create()
    token = await create_access_token(user=user)

    response = await client.get(
        api_router.url_path_for("get_segment", segment_id=10),
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.parametrize("is_admin", [True])
@pytest.mark.parametrize("email_verified_at", [datetime.now()])
async def test_store_view_should_update_segment(
    client: AsyncClient, is_admin, email_verified_at
):
    """Test store view should update segment only by admin."""
    user = await UserFactory.create(
        is_admin=is_admin, email_verified_at=email_verified_at
    )
    token = await create_access_token(user=user)

    segment = await SegmentFactory.create()
    build = await SegmentFactory.build()
    data = {
        "title": build.title,
        "is_active": build.is_active,
        "image": build.image,
        "color": build.color,
    }

    response = await client.put(
        api_router.url_path_for("update_segment", segment_id=segment.id),
        headers={"Authorization": f"Bearer {token['access_token']}"},
        json=data,
    )

    if is_admin and email_verified_at is not None:
        assert response.status_code == status.HTTP_200_OK
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.parametrize("is_admin", [True])
@pytest.mark.parametrize("email_verified_at", [datetime.now()])
async def test_store_view_should_delete_segment(
    client: AsyncClient, is_admin, email_verified_at
):
    """Test store view should delete segment only by admin."""
    user = await UserFactory.create(
        is_admin=is_admin, email_verified_at=email_verified_at
    )
    token = await create_access_token(user=user)

    segment = await SegmentFactory.create()

    response = await client.delete(
        api_router.url_path_for("delete_segment", segment_id=segment.id),
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    if is_admin and email_verified_at is not None:
        assert response.status_code == status.HTTP_204_NO_CONTENT
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN
