from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.store.models import Segment
from app.store.schemas import SegmentCreate, SegmentUpdate


async def create(
    *,
    session: AsyncSession,
    segment_in: SegmentCreate,
):
    """Create a new segment."""
    create_data = segment_in.dict()

    instance = Segment(**create_data)
    session.add(instance)
    await session.commit()

    return instance


async def get(
    *,
    session: AsyncSession,
    segment_id: int,
) -> Optional[Segment]:
    """Get a segment by id."""
    query = await session.execute(select(Segment).filter_by(id=segment_id))
    segment = query.scalar_one_or_none()
    await session.commit()

    return segment


async def update(
    *, session: AsyncSession, segment: Segment, segment_in: SegmentUpdate
):
    """Update a segment."""
    segment_data = jsonable_encoder(segment)
    update_data = segment_in.dict(exclude_unset=True)

    for field in segment_data:
        if field in update_data:
            setattr(segment, field, update_data[field])

    await session.commit()

    return segment


async def delete(*, session: AsyncSession, segment: Segment):
    """Delete a segment."""
    await session.delete(segment)
    await session.commit()
