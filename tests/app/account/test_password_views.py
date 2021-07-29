import pprint

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.future import select

from app.account.schemas import PasswordResetTokenCreate
from app.account.services.password import create_reset
from app.auth.services import authenticate_user, create_access_token
from app.database import async_session
from app.main import api_router
from app.user.models import PasswordReset
from tests.app.user.factories import UserFactory
from tests.utils import vcr


@pytest.mark.asyncio
@vcr.use_cassette()
async def test_account_view_should_create_password_reset_token(
    client: AsyncClient,
):
    """Test account view should create password reset token."""
    user = await UserFactory.create()
    token = await create_access_token(user=user)

    data = {
        "email": user.email,
    }

    response = await client.post(
        api_router.url_path_for("create_password_reset_token"),
        json=data,
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    async with async_session() as session:
        query = await session.execute(
            select(PasswordReset).filter_by(email=user.email)
        )
        instance = query.scalar_one_or_none()
        await session.commit()
        assert instance is not None

    assert response.status_code == status.HTTP_202_ACCEPTED


@pytest.mark.asyncio
@vcr.use_cassette()
async def test_account_view_should_form_password_reset(client: AsyncClient):
    """Test account view should form password reset."""
    user = await UserFactory.create()
    reset_in = PasswordResetTokenCreate(**{"email": user.email})

    pprint.pp("*****************")
    pprint.pp(user.password)
    pprint.pp("*****************")

    async with async_session() as session:
        instance = await create_reset(session=session, reset_in=reset_in)

        response = await client.get(
            api_router.url_path_for("password_reset_form"),
            params={"token": instance.token, "email": user.email},
        )
        assert response.status_code == status.HTTP_200_OK

        response = await client.post(
            api_router.url_path_for("password_reset_form"),
            params={"token": instance.token, "email": user.email},
            data={
                "token": instance.token,
                "email": user.email,
                "password": "password_updated",
                "confirm": "password_updated",
            },
        )

        changed = await authenticate_user(
            session=session,
            username=user.email,
            password="password_updated",
        )
        assert changed is not False
