from typing import List

from sqlalchemy.future import select

from app.config import get_settings
from app.core.filters.filters import apply_filters
from app.core.filters.sorting import apply_sort
from app.core.pagination import apply_pagination

settings = get_settings()


async def search_filter_sort_paginate(
    session,
    model,
    filter_spec: List[dict] = None,
    page: int = 1,
    items_per_page: int = settings.DEFAULT_ITEMS_PER_PAGE,
    sort_spec: List[str] = None,
):
    """Common functionality for
    searching, filtering, sorting, and pagination."""
    stmt = select(model)

    if filter_spec:
        stmt = apply_filters(stmt, filter_spec)

    if sort_spec:
        stmt = apply_sort(stmt, sort_spec)

    if items_per_page == -1:
        items_per_page = None
    elif items_per_page > settings.MAX_ITEMS_PER_PAGE:
        items_per_page = settings.MAX_ITEMS_PER_PAGE

    stmt, pagination = await apply_pagination(
        stmt,
        session=session,
        page_number=page,
        page_size=items_per_page,
    )

    query = await session.execute(stmt)
    await session.commit()

    return {
        "items": query.scalars().all(),
        "per_page": pagination.page_size,
        "num_pages": pagination.num_pages,
        "page": pagination.page_number,
        "total": pagination.total_results,
    }
