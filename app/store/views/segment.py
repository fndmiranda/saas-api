import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.depends import current_user_admin, current_user_verified
from app.core.depends import pagination_parameters
from app.core.services import search_filter_sort_paginate
from app.depends import get_session
from app.store.models import Segment as SegmentModel
from app.store.schemas import (
    Segment,
    SegmentCreate,
    SegmentPagination,
    SegmentUpdate,
)
from app.store.services.segment import create, delete, get, update
from app.store.validators import validate_segment

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/segments",
    summary="Create segment.",
    response_model=Segment,
    dependencies=[Depends(current_user_admin)],
    status_code=status.HTTP_201_CREATED,
)
async def create_segment(
    *, session: AsyncSession = Depends(get_session), segment_in: SegmentCreate
):
    logger.info(
        "Starting create segment with={}".format(
            {
                "segment_in": segment_in,
            }
        )
    )

    await validate_segment(session=session, segment_in=segment_in)

    segment = await create(session=session, segment_in=segment_in)
    logger.info(
        "Segment created successfully with={}".format(
            {
                "segment": segment,
            }
        )
    )
    return segment


@router.get(
    "/segments",
    summary="Get segments.",
    response_model=SegmentPagination,
)
async def get_segments(
    *,
    session: AsyncSession = Depends(get_session),
    common: dict = Depends(pagination_parameters),
):
    logger.info(f"Starting get segments with={common}")

    pagination = await search_filter_sort_paginate(
        session=session, model=SegmentModel, **common
    )

    logger.info(
        "Segments got successfully with={}".format(
            {
                "page": pagination["page"],
                "items": len(pagination["items"]),
                "per_page": pagination["per_page"],
                "parameters": common,
                "num_pages": pagination["num_pages"],
                "total": pagination["total"],
            }
        )
    )

    return pagination


@router.get(
    "/segments/{segment_id}",
    summary="Get segment.",
    dependencies=[Depends(current_user_verified)],
    response_model=Segment,
)
async def get_segment(
    *, session: AsyncSession = Depends(get_session), segment_id: int
):
    logger.info(
        "Starting get segment with={}".format(
            {
                "segment_id": segment_id,
            }
        )
    )

    segment = await get(session=session, segment_id=segment_id)

    if not segment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found."
        )

    logger.info(
        "Segment got successfully with={}".format(
            {
                "segment": segment,
            }
        )
    )

    return segment


@router.put(
    "/segments/{segment_id}",
    summary="Update segment.",
    response_model=Segment,
    dependencies=[Depends(current_user_admin)],
)
async def update_segment(
    *,
    session: AsyncSession = Depends(get_session),
    segment_id: int,
    segment_in: SegmentUpdate,
):
    logger.info(
        "Starting update segment with={}".format(
            {
                "segment_id": segment_id,
                "segment_in": segment_in,
            }
        )
    )

    segment = await get(session=session, segment_id=segment_id)

    if not segment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found."
        )

    await validate_segment(
        session=session, segment_in=segment_in, segment=segment
    )

    segment = await update(
        session=session, segment_in=segment_in, segment=segment
    )
    logger.info(
        "Segment updated successfully with={}".format(
            {
                "segment": segment.dict(),
            }
        )
    )
    return segment


@router.delete(
    "/segments/{segment_id}",
    summary="Delete segment.",
    dependencies=[Depends(current_user_admin)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_segment(
    *,
    session: AsyncSession = Depends(get_session),
    segment_id: int,
):
    logger.info(
        "Starting delete segment with={}".format({"segment_id": segment_id})
    )

    segment = await get(session=session, segment_id=segment_id)

    if not segment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found."
        )

    await delete(session=session, segment=segment)

    logger.info(
        "Segment deleted successfully with={}".format(
            {
                "segment_id": segment_id,
            }
        )
    )

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
