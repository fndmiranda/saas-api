import os
from typing import Generator

import pytest
from httpx import AsyncClient

from alembic import command
from alembic.config import Config
from app.config import Settings
from app.depends import get_settings
from app.main import app

pytest_plugins = [
    "tests.app.account.fixtures",
]


def get_settings_override():
    return Settings(
        SQLALCHEMY_DATABASE_URI="sqlite+aiosqlite:///./instance/testing.db",
        ADMIN_EMAIL="testing_admin@example.com",
        TESTING=True,
    )


app.dependency_overrides[get_settings] = get_settings_override


@pytest.fixture()
def app() -> Generator:
    from app.main import app

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    yield app

    try:
        os.unlink("instance/testing.db")
    except OSError:
        pass


@pytest.fixture()
async def client(app) -> Generator:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
