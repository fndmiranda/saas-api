import pytest

from app.user.models import User


@pytest.mark.asyncio
async def test_core_model_should_model_mixin(account_create_body):
    """Test core model should model mixin."""

    user = User(**account_create_body)

    assert isinstance(user.to_dict(), dict)
