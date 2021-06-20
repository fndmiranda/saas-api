from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.account.schemas import Account
from app.user.models import User


async def validate_account(
    *, session: AsyncSession, account_in: Account, account: Account = None
):
    clauses = (
        User.email == account_in.email,
        User.nickname == account_in.nickname,
        User.document_number == account_in.document_number,
    )

    stmt = select(User).where(or_(*clauses))

    if account is not None:
        stmt = stmt.where(User.id != account.id)

    query = await session.execute(stmt)
    user = query.scalar_one_or_none()
    await session.commit()

    if user is not None:
        detail = []

        for clause in clauses:
            if getattr(account_in, clause.left.name) == clause.right.value:
                detail.append(
                    {
                        "loc": ["body", clause.left.name],
                        "msg": "already exists",
                        "type": "value_error.unique",
                    }
                )

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )
