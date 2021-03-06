import pytest
from pydantic import ValidationError

from app.account.schemas import AccountCreate


@pytest.mark.asyncio
async def test_account_schema_not_should_with_legal_term_not_accept(
    account_primary: dict,
):
    """Test oauth service not should authenticate user with
    legal term not accept.
    """

    account_primary.update({"accept_legal_term": False})
    with pytest.raises(ValidationError):
        AccountCreate(**account_primary)
