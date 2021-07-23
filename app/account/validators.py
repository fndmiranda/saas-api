from fastapi import HTTPException, status
from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.account.schemas import Account
from app.user.models import User


async def validate_account(
    *, session: AsyncSession, account_in: Account, account: Account = None
):
    clauses = []
    for field in ["email", "nickname", "document_number"]:
        if getattr(account_in, field) is not None:
            clauses.append(
                getattr(User, field) == getattr(account_in, field)
            )

    if not len(clauses):
        return

    stmt = select(User).where(or_(*clauses))

    if account is not None:
        stmt = stmt.where(User.id != account.id)

    query = await session.execute(stmt.with_only_columns(func.count()))

    await session.commit()

    if query.scalar_one():
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
