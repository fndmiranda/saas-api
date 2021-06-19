import pytest

from app.config import Settings
from app.depends import get_settings


@pytest.mark.asyncio
async def test_dependencies_should_get_settings():
    """Test dependencies should get settings."""

    settings = get_settings()

    assert isinstance(settings, Settings)
