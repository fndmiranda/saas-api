from fastapi import HTTPException, status
from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.store.models import Segment as SegmentModel
from app.store.schemas import Segment


async def validate_segment(
    *, session: AsyncSession, segment_in: Segment, segment: Segment = None
):
    clauses = (SegmentModel.title == segment_in.title,)
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
