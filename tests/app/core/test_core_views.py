import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from app.depends import get_settings
from app.main import api_router
from app.version import __version__


@pytest.mark.asyncio
async def test_read_app(app: FastAPI):
    assert app.version == __version__


@pytest.mark.asyncio
async def test_core_view_should_health_check(client: AsyncClient):
    response = await client.get(api_router.url_path_for("health_check"))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_core_view_should_root(client: AsyncClient):
    response = await client.get(api_router.url_path_for("root"))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "application": f"{get_settings().APP_NAME} - {__version__}"
    }
