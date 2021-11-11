import pytest

from app.user.models import User


@pytest.mark.asyncio
async def test_core_model_should_model_mixin(account_primary):
    """Test core model should model mixin."""

    user = User(**account_primary)

    assert isinstance(user.dict(), dict)
