import hashlib
from hmac import compare_digest

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.account.schemas import AccountEmailVerify
from app.user.models import User


async def mark_email_as_verified(
    *, session: AsyncSession, account: User, verify_in: AccountEmailVerify
):
    """Mark a account email verified."""
    account_data = jsonable_encoder(account)
    update_data = verify_in.dict(exclude_unset=True)

    for field in account_data:
        if field in update_data:
            setattr(account, field, update_data[field])

    await session.commit()

    return account


async def get_signature(account: User):
    """Get the signature."""
    word = "{}-{}".format(
        account.created_at.timestamp(), account.salt
    ).encode()
    return hashlib.sha256(word).hexdigest()


async def signature_is_valid(account: User, signature: str):
    """Determine if the signature is valid."""
    return compare_digest(await get_signature(account=account), signature)


async def generate_verify_email_url(*, account: User, request: Request):
    """Generate verify email url."""
    logger.info(
        "Starting generate email verify url with={}".format(
            {
                "user_id": account.id,
            }
        )
    )

    url = request.url_for(
        "email_verify",
        user_id=account.id,
        signature=await get_signature(account=account),
    )

    logger.info(
        "Verify email url generated successfully with={}".format(
            {
                "user_id": account.id,
            }
        )
    )
    return url
