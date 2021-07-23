from fastapi import HTTPException, status
from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.account.schemas import Account
from app.store.models import Segment as SegmentModel
from app.store.models import Store as StoreModel
from app.store.models import StorePerson
from app.store.schemas import Segment, Store


async def validate_segment(
    *, session: AsyncSession, segment_in: Segment, segment: Segment = None
):
    clauses = []
    for field in ["title"]:
        if getattr(segment_in, field) is not None:
            clauses.append(
                getattr(SegmentModel, field) == getattr(segment_in, field)
            )

    if not len(clauses):
        return

    stmt = select(SegmentModel).where(or_(*clauses))

    if segment is not None:
        stmt = stmt.where(SegmentModel.id != segment.id)

    query = await session.execute(stmt.with_only_columns(func.count()))

    await session.commit()

    if query.scalar_one():
        detail = []
        for clause in clauses:
            if getattr(segment_in, clause.left.name) == clause.right.value:
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


async def validate_store(
    *, session: AsyncSession, store_in: Store, store: Store = None
):
    clauses = []
    for field in ["title", "legal", "document_number"]:
        if getattr(store_in, field) is not None:
            clauses.append(
                getattr(StoreModel, field) == getattr(store_in, field)
            )

    if not len(clauses):
        return

    stmt = select(StoreModel).where(or_(*clauses))

    if store is not None:
        stmt = stmt.where(StoreModel.id != store.id)

    query = await session.execute(stmt.with_only_columns(func.count()))

    await session.commit()

    if query.scalar_one():
        detail = []
        for clause in clauses:
            if getattr(store_in, clause.left.name) == clause.right.value:
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


async def validate_store_owner_or_admin(
    *, session: AsyncSession, account: Account, store: Store
):
    stmt = select(StorePerson).where(
        StorePerson.user_id == account.id,
        StorePerson.store_id == store.id,
        StorePerson.is_owner,
        StorePerson.is_active,
    )
    query = await session.execute(stmt.with_only_columns(func.count()))
    await session.commit()

    if not query.scalar_one() and not account.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden."
        )
