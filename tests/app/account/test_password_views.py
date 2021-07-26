import json
import pprint
from datetime import datetime
from unittest.mock import patch

import pytest
from fastapi import status
from httpx import AsyncClient

from app.account.services.account import get
from app.auth.services import create_access_token
from app.database import async_session
from app.main import api_router
from tests.app.address.factories import AddressFactory
from tests.app.user.factories import UserFactory
from tests.utils import vcr
from app.user.models import PasswordReset
from sqlalchemy.future import select


@pytest.mark.asyncio
@vcr.use_cassette()
async def test_account_view_should_create_password_reset_token(
    client: AsyncClient
):
    """Test account view should create password reset token."""
    user = await UserFactory.create()
    token = await create_access_token(user=user)

    data = {
        "email": user.email,
    }

    response = await client.post(
        api_router.url_path_for("create_password_reset_token"), json=data,
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    pprint.pp("****************")
    pprint.pp(response)
    pprint.pp(response.json())
    pprint.pp("****************")

    async with async_session() as session:
        query = await session.execute(select(PasswordReset).filter_by(
            email=user.email
        ))
        instance = query.scalar_one_or_none()
        await session.commit()

        assert instance is not None

    assert response.status_code == status.HTTP_202_ACCEPTED


# @pytest.mark.asyncio
# @pytest.mark.parametrize("email_verified_at", [None, datetime.now()])
# async def test_account_view_should_get_addresses(
#     client: AsyncClient,
#     email_verified_at,
# ):
#     """Test account view should get account addresses."""
#     user = await UserFactory.create(email_verified_at=email_verified_at)
#     token = await create_access_token(user=user)
#     addresses = await AddressFactory.create_batch(
#         3,
#         parent_id=user.id,
#         discriminator=user.__class__.__name__.lower(),
#         state="MG",
#     )
#
#     filter_spec = [
#         {
#             "model": "Address",
#             "field": "state",
#             "op": "eq",
#             "value": "MG",
#         }
#     ]
#     sort_spec = [{"model": "Address", "field": "id", "direction": "desc"}]
#
#     response = await client.get(
#         api_router.url_path_for("get_account_addresses"),
#         headers={"Authorization": f"Bearer {token['access_token']}"},
#         params={
#             "filter": json.dumps(filter_spec),
#             "sort": json.dumps(sort_spec),
#         },
#     )
#
#     if email_verified_at is not None:
#         assert response.status_code == status.HTTP_200_OK
#         assert response.json()["total"] == len(addresses)
#     else:
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize("email_verified_at", [None, datetime.now()])
# async def test_account_view_should_get_address(
#     client: AsyncClient, email_verified_at
# ):
#     """Test account view should get address."""
#     user = await UserFactory.create(email_verified_at=email_verified_at)
#     token = await create_access_token(user=user)
#     address = await AddressFactory.create(
#         parent_id=user.id,
#         discriminator=user.__class__.__name__.lower(),
#     )
#
#     response = await client.get(
#         api_router.url_path_for("get_account_address", address_id=address.id),
#         headers={"Authorization": f"Bearer {token['access_token']}"},
#     )
#
#     if email_verified_at is not None:
#         assert response.status_code == status.HTTP_200_OK
#     else:
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize("email_verified_at", [None, datetime.now()])
# async def test_account_view_should_update_address(
#     client: AsyncClient, email_verified_at
# ):
#     """Test account view should update store by owner."""
#     user = await UserFactory.create(email_verified_at=email_verified_at)
#     token = await create_access_token(user=user)
#     address = await AddressFactory.create(
#         parent_id=user.id,
#         discriminator=user.__class__.__name__.lower(),
#     )
#
#     build = await AddressFactory.build()
#     data = {
#         "name": build.name,
#         "is_default": build.is_default,
#         "street": build.street,
#         "neighborhood": build.neighborhood,
#         "city": build.city,
#         "postcode": build.postcode,
#         "state": build.state,
#         "number": build.number,
#         "complement": build.complement,
#         "lat": build.lat,
#         "lng": build.lng,
#     }
#
#     response = await client.put(
#         api_router.url_path_for(
#             "update_account_address", address_id=address.id
#         ),
#         headers={"Authorization": f"Bearer {token['access_token']}"},
#         json=data,
#     )
#
#     if email_verified_at is not None:
#         assert response.status_code == status.HTTP_200_OK
#     else:
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize("email_verified_at", [None, datetime.now()])
# async def test_account_view_should_delete_address(
#     client: AsyncClient, email_verified_at
# ):
#     """Test account view should delete address by owner."""
#     user = await UserFactory.create(email_verified_at=email_verified_at)
#     token = await create_access_token(user=user)
#     address = await AddressFactory.create(
#         parent_id=user.id,
#         discriminator=user.__class__.__name__.lower(),
#     )
#
#     response = await client.delete(
#         api_router.url_path_for(
#             "delete_account_address", address_id=address.id
#         ),
#         headers={"Authorization": f"Bearer {token['access_token']}"},
#     )
#
#     if email_verified_at is not None:
#         assert response.status_code == status.HTTP_204_NO_CONTENT
#     else:
#         assert response.status_code == status.HTTP_403_FORBIDDEN
